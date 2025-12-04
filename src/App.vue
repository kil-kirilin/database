<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <div class="header-title">
          <h1>📦 Учет материалов 2025</h1>
          <p class="subtitle">Управление расходом материалов с автоматическим подсчетом</p>
        </div>
        <div class="header-stats">
          <div class="stat-item">
            <span class="stat-icon">📊</span>
            <div class="stat-info">
              <span class="stat-label">Записей</span>
              <span class="stat-value">{{ columns.length }}</span>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">💰</span>
            <div class="stat-info">
              <span class="stat-label">Сумма</span>
              <span class="stat-value">{{ formatCurrency(totalYearlyPrice) }}</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="app-main">
      <!-- Панель управления -->
      <div class="control-panel">
        <div class="control-group">
          <button @click="exportToExcel" class="control-btn excel-btn">
            <span class="btn-icon">📥</span>
            Экспорт Excel
          </button>
          <button @click="exportSummary" class="control-btn summary-btn">
            <span class="btn-icon">📈</span>
            Экспорт итогов
          </button>
          <button @click="exportCSV" class="control-btn csv-btn">
            <span class="btn-icon">📄</span>
            Экспорт CSV
          </button>
          <button @click="refreshData" class="control-btn refresh-btn">
            <span class="btn-icon">🔄</span>
            Обновить
          </button>
        </div>
        
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Поиск материалов..." 
            class="search-input"
          />
          <span class="search-icon">🔍</span>
        </div>
      </div>

      <!-- Форма добавления -->
      <section class="form-section">
        <div class="section-header" @click="toggleForm">
          <h2>Добавить новый материал</h2>
          <span class="section-icon">{{ formExpanded ? '−' : '+' }}</span>
        </div>
        
        <transition name="slide">
          <form v-if="formExpanded" @submit.prevent="addItem" class="add-form">
            <div class="form-grid">
              <div class="form-group" v-for="header in headersWithoutNote" :key="header.name">
                <label :for="header.name" class="form-label">
                  {{ header.display }}
                  <span v-if="isRequiredField(header.name)" class="required">*</span>
                </label>
                <input 
                  v-model="newItem[header.name]" 
                  :id="header.name" 
                  :type="getInputType(header.name)" 
                  :placeholder="getPlaceholder(header.name)"
                  :required="isRequiredField(header.name)"
                  class="form-input"
                />
              </div>
              <div class="form-group full-width">
                <label for="note">Примечание</label>
                <textarea 
                  v-model="newItem.note" 
                  id="note" 
                  placeholder="Дополнительная информация"
                  class="form-input"
                  rows="2"
                ></textarea>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="submit" class="submit-btn">
                <span class="btn-icon">✓</span>
                {{ editMode ? 'Обновить материал' : 'Добавить материал' }}
              </button>
              <button type="button" @click="clearForm" class="clear-btn">
                <span class="btn-icon">✕</span>
                Очистить
              </button>
            </div>
          </form>
        </transition>
      </section>

      <!-- Таблица данных -->
      <section class="table-section">
        <div class="table-header">
          <h2>Таблица расходов материалов</h2>
          <div class="table-info">
            <span class="info-item">Показано: {{ filteredColumns.length }} из {{ columns.length }}</span>
            <span class="info-item">Обновлено: {{ lastUpdate }}</span>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th v-for="header in headers" :key="header.name" class="table-header-cell" :class="getHeaderClass(header.name)">
                  <div class="header-content">
                    {{ header.display }}
                  </div>
                </th>
                <th class="table-header-cell actions-header">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="column in filteredColumns" :key="column.number" class="table-row">
                <td v-for="header in headers" :key="header.name" class="table-cell" :class="getCellClass(header.name)">
                  <div class="cell-content" :title="column[header.name]">
                    {{ formatCellValue(column[header.name], header.name) }}
                  </div>
                </td>
                <td class="table-cell actions-cell">
                  <div class="action-buttons">
                    <button @click="editItem(column)" class="action-btn edit-btn" title="Редактировать">
                      <span class="btn-icon">✏️</span>
                    </button>
                    <button @click="deleteItem(column.number)" class="action-btn delete-btn" title="Удалить">
                      <span class="btn-icon">🗑️</span>
                    </button>
                  </div>
                </td>
              </tr>
              
              <tr v-if="filteredColumns.length === 0" class="empty-row">
                <td :colspan="headers.length + 1" class="empty-cell">
                  <div class="empty-state">
                    <span class="empty-icon">📝</span>
                    <p>{{ searchQuery ? 'Ничего не найдено' : 'Нет данных. Добавьте первый материал.' }}</p>
                    <button v-if="searchQuery" @click="clearSearch" class="clear-search-btn">
                      Очистить поиск
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
            
            <!-- Итоговая строка -->
            <tfoot class="table-footer">
              <tr>
                <td class="footer-label">Итого:</td>
                <td class="footer-empty">—</td>
                <td class="footer-total total-quantity">{{ totalQuantity.toLocaleString('ru-RU') }}</td>
                <td class="footer-total total-consumption">{{ totalMonthlyConsumption.toLocaleString('ru-RU') }}</td>
                <td class="footer-total total-consumption">{{ totalYearlyConsumption.toLocaleString('ru-RU') }}</td>
                <td class="footer-total total-price">{{ formatCurrency(totalMonthlyPrice) }}</td>
                <td class="footer-total total-price">{{ formatCurrency(totalYearlyPrice) }}</td>
                <td class="footer-actions">—</td>
              </tr>
            </tfoot>
          </table>
        </div>

        <!-- Статистика -->
        <div class="summary-cards">
          <div v-for="(summary, index) in summaryData" :key="index" class="summary-card" :class="`card-${index}`">
            <div class="card-icon">{{ summary.icon }}</div>
            <div class="card-content">
              <h3 class="card-title">{{ summary.title }}</h3>
              <p class="card-value">{{ summary.value }}</p>
              <span class="card-unit">{{ summary.unit }}</span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="app-footer">
      <div class="footer-content">
        <p class="copyright">© 2025 Система учета материалов v1.0</p>
        <div class="footer-info">
          <span class="info-item">Всего записей: {{ columns.length }}</span>
          <span class="info-item">Общая стоимость: {{ formatCurrency(totalYearlyPrice) }}</span>
          <span class="info-item">Последнее обновление: {{ lastUpdate }}</span>
        </div>
      </div>
    </footer>

    <!-- Уведомления -->
    <transition name="fade">
      <div v-if="notification.show" class="notification" :class="`notification-${notification.type}`">
        <span class="notification-icon">{{ notification.icon }}</span>
        <div class="notification-content">
          <p class="notification-title">{{ notification.title }}</p>
          <p class="notification-message">{{ notification.message }}</p>
        </div>
        <button @click="hideNotification" class="notification-close">×</button>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

export default {
  name: 'App',
  data() {
    return {
      headers: [
        { name: 'number', display: '№' },
        { name: 'name', display: 'Наименование' },
        { name: 'quantity', display: 'Кол-во' },
        { name: 'monthlyConsumption', display: 'Расход/мес' },
        { name: 'yearlyConsumption', display: 'Расход/год' },
        { name: 'monthlyPrice', display: 'Цена/мес (₽)' },
        { name: 'yearlyPrice', display: 'Цена/год (₽)' },
        { name: 'note', display: 'Примечание' }
      ],
      columns: [],
      newItem: {
        number: '',
        name: '',
        quantity: '',
        monthlyConsumption: '',
        yearlyConsumption: '',
        monthlyPrice: '',
        yearlyPrice: '',
        note: ''
      },
      searchQuery: '',
      formExpanded: true,
      lastUpdate: '—',
      notification: {
        show: false,
        type: 'info',
        title: '',
        message: '',
        icon: 'ℹ️'
      },
      editMode: false,
      editingId: null
    };
  },
  computed: {
    headersWithoutNote() {
      return this.headers.filter(header => header.name !== 'note');
    },
    
    filteredColumns() {
      if (!this.searchQuery) {
        return this.columns;
      }
      const query = this.searchQuery.toLowerCase();
      return this.columns.filter(item => {
        return Object.values(item).some(value => 
          String(value).toLowerCase().includes(query)
        );
      });
    },
    
    totalQuantity() {
      let sum = 0;
      for (let i = 0; i < this.columns.length; i++) {
        sum += parseFloat(this.columns[i].quantity) || 0;
      }
      return sum;
    },
    
    totalMonthlyConsumption() {
      let sum = 0;
      for (let i = 0; i < this.columns.length; i++) {
        sum += parseFloat(this.columns[i].monthlyConsumption) || 0;
      }
      return sum;
    },
    
    totalYearlyConsumption() {
      let sum = 0;
      for (let i = 0; i < this.columns.length; i++) {
        sum += parseFloat(this.columns[i].yearlyConsumption) || 0;
      }
      return sum;
    },
    
    totalMonthlyPrice() {
      let sum = 0;
      for (let i = 0; i < this.columns.length; i++) {
        sum += parseFloat(this.columns[i].monthlyPrice) || 0;
      }
      return sum;
    },
    
    totalYearlyPrice() {
      let sum = 0;
      for (let i = 0; i < this.columns.length; i++) {
        sum += parseFloat(this.columns[i].yearlyPrice) || 0;
      }
      return sum;
    },
    
    summaryData() {
      return [
        {
          icon: '📦',
          title: 'Всего материалов',
          value: this.columns.length,
          unit: 'шт'
        },
        {
          icon: '💰',
          title: 'Общая стоимость',
          value: this.formatCurrency(this.totalYearlyPrice),
          unit: ''
        },
        {
          icon: '📈',
          title: 'Средний расход',
          value: this.columns.length > 0 ? 
            Math.round(this.totalMonthlyConsumption / this.columns.length * 100) / 100 : 0,
          unit: 'ед/мес'
        },
        {
          icon: '⚡',
          title: 'Эффективность',
          value: this.columns.length > 0 ? 
            Math.round((this.totalYearlyPrice / this.totalQuantity) * 100) / 100 : 0,
          unit: '₽/ед'
        }
      ];
    }
  },
  methods: {
    async fetchItems() {
      try {
        this.showNotification('Загрузка данных...', 'info', '⏳');
        const response = await axios.get('http://localhost:5000/api/data');
        this.columns = response.data;
        this.updateTimestamp();
        this.showNotification('Данные успешно загружены', 'success', '✅');
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
        this.showNotification('Ошибка загрузки данных', 'error', '❌');
      }
    },
    
    async addItem() {
      if (!this.validateForm()) {
        this.showNotification('Заполните все обязательные поля', 'warning', '⚠️');
        return;
      }
      
      try {
        const itemToSend = { ...this.newItem };
        const numericFields = ['quantity', 'monthlyConsumption', 'yearlyConsumption', 'monthlyPrice', 'yearlyPrice'];
        
        for (let i = 0; i < numericFields.length; i++) {
          const field = numericFields[i];
          if (itemToSend[field]) {
            itemToSend[field] = parseFloat(itemToSend[field]) || 0;
          }
        }
        
        if (this.editMode && this.editingId) {
          await axios.put(`http://localhost:5000/api/data/${this.editingId}`, itemToSend);
          this.showNotification('Материал обновлен', 'success', '✓');
        } else {
          await axios.post('http://localhost:5000/api/data', itemToSend);
          this.showNotification('Материал добавлен', 'success', '✓');
        }
        
        this.fetchItems();
        this.clearForm();
      } catch (error) {
        console.error('Ошибка при сохранении элемента:', error);
        this.showNotification('Ошибка сохранения', 'error', '❌');
      }
    },
    
    clearForm() {
      this.newItem = {
        number: '',
        name: '',
        quantity: '',
        monthlyConsumption: '',
        yearlyConsumption: '',
        monthlyPrice: '',
        yearlyPrice: '',
        note: ''
      };
      this.editMode = false;
      this.editingId = null;
    },
    
    editItem(item) {
      this.newItem = { ...item };
      this.editMode = true;
      this.editingId = item.number;
      this.formExpanded = true;
      this.showNotification('Режим редактирования', 'info', '✏️');
    },
    
    async deleteItem(itemNumber) {
      if (!confirm(`Удалить материал №${itemNumber}?`)) return;
      
      try {
        await axios.delete(`http://localhost:5000/api/data/${itemNumber}`);
        this.fetchItems();
        this.showNotification('Материал удален', 'success', '🗑️');
      } catch (error) {
        console.error('Ошибка при удалении элемента:', error);
        this.showNotification('Ошибка удаления', 'error', '❌');
      }
    },
    
    validateForm() {
      const requiredFields = ['number', 'name', 'quantity', 'monthlyPrice'];
      for (let i = 0; i < requiredFields.length; i++) {
        const field = requiredFields[i];
        if (!this.newItem[field] || this.newItem[field].toString().trim() === '') {
          return false;
        }
      }
      return true;
    },
    
    isRequiredField(fieldName) {
      const requiredFields = ['number', 'name', 'quantity', 'monthlyPrice'];
      return requiredFields.includes(fieldName);
    },
    
    getInputType(fieldName) {
      const numericFields = ['quantity', 'monthlyConsumption', 'yearlyConsumption', 'monthlyPrice', 'yearlyPrice'];
      return numericFields.includes(fieldName) ? 'number' : 'text';
    },
    
    getPlaceholder(fieldName) {
      const placeholders = {
        number: 'Введите номер',
        name: 'Наименование материала',
        quantity: 'Количество',
        monthlyConsumption: 'Расход в месяц',
        yearlyConsumption: 'Расход в год',
        monthlyPrice: 'Цена за месяц',
        yearlyPrice: 'Цена за год',
        note: 'Дополнительная информация'
      };
      return placeholders[fieldName] || '';
    },
    
    // ========== ЭКСПОРТ В EXCEL ==========
    exportToExcel() {
      try {
        const exportData = this.prepareExportData();
        const date = new Date();
        const filename = `материалы_${date.getFullYear()}_${date.getMonth()+1}_${date.getDate()}.xlsx`;
        
        // Создаем книгу Excel
        const workbook = XLSX.utils.book_new();
        
        // Создаем лист с данными
        const worksheet = XLSX.utils.json_to_sheet(exportData);
        
        // Настраиваем ширину колонок
        const wscols = [
          { wch: 8 },  // №
          { wch: 30 }, // Наименование
          { wch: 10 }, // Кол-во
          { wch: 15 }, // Расход/мес
          { wch: 15 }, // Расход/год
          { wch: 15 }, // Цена/мес
          { wch: 15 }, // Цена/год
          { wch: 25 }  // Примечание
        ];
        worksheet['!cols'] = wscols;
        
        // Добавляем лист в книгу
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Материалы');
        
        // Создаем лист с итогами
        const summaryData = this.prepareSummaryData();
        const summarySheet = XLSX.utils.json_to_sheet(summaryData);
        XLSX.utils.book_append_sheet(workbook, summarySheet, 'Итоги');
        
        // Генерируем и сохраняем файл
        const excelBuffer = XLSX.write(workbook, { 
          bookType: 'xlsx', 
          type: 'array' 
        });
        
        const dataBlob = new Blob([excelBuffer], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });
        
        saveAs(dataBlob, filename);
        this.showNotification('Excel файл экспортирован', 'success', '📥');
      } catch (error) {
        console.error('Ошибка экспорта в Excel:', error);
        this.showNotification('Ошибка экспорта', 'error', '❌');
      }
    },
    
    exportSummary() {
      try {
        const summaryData = this.prepareSummaryData();
        const date = new Date();
        const filename = `сводка_материалов_${date.getFullYear()}_${date.getMonth()+1}_${date.getDate()}.xlsx`;
        
        const workbook = XLSX.utils.book_new();
        const worksheet = XLSX.utils.json_to_sheet(summaryData);
        
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Сводка');
        
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const dataBlob = new Blob([excelBuffer], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });
        
        saveAs(dataBlob, filename);
        this.showNotification('Сводка экспортирована', 'success', '📈');
      } catch (error) {
        console.error('Ошибка экспорта сводки:', error);
        this.showNotification('Ошибка экспорта', 'error', '❌');
      }
    },
    
    exportCSV() {
      try {
        const exportData = this.prepareExportData();
        const headers = Object.keys(exportData[0] || {});
        const csvRows = [];
        
        // Заголовки
        csvRows.push(headers.join(';'));
        
        // Данные
        exportData.forEach(row => {
          const values = headers.map(header => {
            const value = row[header];
            const escaped = ('' + value).replace(/"/g, '""');
            return `"${escaped}"`;
          });
          csvRows.push(values.join(';'));
        });
        
        const csvString = csvRows.join('\n');
        const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
        const date = new Date();
        const filename = `материалы_${date.getFullYear()}_${date.getMonth()+1}_${date.getDate()}.csv`;
        
        saveAs(blob, filename);
        this.showNotification('CSV файл экспортирован', 'success', '📄');
      } catch (error) {
        console.error('Ошибка экспорта в CSV:', error);
        this.showNotification('Ошибка экспорта', 'error', '❌');
      }
    },
    
    prepareExportData() {
      return this.columns.map(item => {
        return {
          '№': item.number,
          'Наименование': item.name,
          'Кол-во': item.quantity,
          'Расход/мес': item.monthlyConsumption,
          'Расход/год': item.yearlyConsumption,
          'Цена/мес (₽)': item.monthlyPrice,
          'Цена/год (₽)': item.yearlyPrice,
          'Примечание': item.note || ''
        };
      });
    },
    
    prepareSummaryData() {
      return [
        { 'Показатель': 'Всего материалов', 'Значение': this.columns.length, 'Единица': 'шт' },
        { 'Показатель': 'Общая стоимость за год', 'Значение': this.totalYearlyPrice, 'Единица': '₽' },
        { 'Показатель': 'Общая стоимость за месяц', 'Значение': this.totalMonthlyPrice, 'Единица': '₽' },
        { 'Показатель': 'Общее количество', 'Значение': this.totalQuantity, 'Единица': 'ед' },
        { 'Показатель': 'Средний расход в месяц', 'Значение': this.columns.length > 0 ? 
            Math.round(this.totalMonthlyConsumption / this.columns.length * 100) / 100 : 0, 
          'Единица': 'ед/мес' },
        { 'Показатель': 'Средняя цена за единицу', 'Значение': this.totalQuantity > 0 ? 
            Math.round(this.totalYearlyPrice / this.totalQuantity * 100) / 100 : 0, 
          'Единица': '₽/ед' }
      ];
    },
    
    // ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========
    updateTimestamp() {
      const now = new Date();
      this.lastUpdate = now.toLocaleTimeString('ru-RU', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      });
    },
    
    refreshData() {
      this.fetchItems();
      this.showNotification('Данные обновлены', 'info', '🔄');
    },
    
    clearSearch() {
      this.searchQuery = '';
    },
    
    toggleForm() {
      this.formExpanded = !this.formExpanded;
    },
    
    formatCurrency(value) {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    },
    
    formatCellValue(value, headerName) {
      if (!value && value !== 0) return '—';
      
      if (headerName.includes('Price')) {
        return this.formatCurrency(parseFloat(value) || 0);
      }
      
      if (headerName === 'quantity' || headerName.includes('Consumption')) {
        const num = parseFloat(value);
        return isNaN(num) ? value : num.toLocaleString('ru-RU');
      }
      
      return value;
    },
    
    getHeaderClass(headerName) {
      return {
        'number-header': headerName === 'number',
        'name-header': headerName === 'name',
        'price-header': headerName.includes('Price'),
        'consumption-header': headerName.includes('Consumption')
      };
    },
    
    getCellClass(headerName) {
      return {
        'number-cell': headerName === 'number',
        'name-cell': headerName === 'name',
        'price-cell': headerName.includes('Price'),
        'consumption-cell': headerName.includes('Consumption'),
        'note-cell': headerName === 'note'
      };
    },
    
    showNotification(title, type = 'info', icon = 'ℹ️') {
      const messages = {
        success: 'Успешно выполнено',
        error: 'Произошла ошибка',
        warning: 'Внимание',
        info: 'Информация'
      };
      
      this.notification = {
        show: true,
        type,
        title: title || messages[type],
        message: this.getNotificationMessage(type),
        icon
      };
      
      // Автоматическое скрытие через 5 секунд
      setTimeout(() => {
        this.hideNotification();
      }, 5000);
    },
    
    getNotificationMessage(type) {
      const messages = {
        success: 'Операция выполнена успешно',
        error: 'Попробуйте еще раз или обратитесь к администратору',
        warning: 'Проверьте введенные данные',
        info: 'Операция в процессе выполнения'
      };
      return messages[type] || '';
    },
    
    hideNotification() {
      this.notification.show = false;
    }
  },
  
  mounted() {
    this.fetchItems();
    // Обновляем время каждую минуту
    setInterval(this.updateTimestamp, 60000);
  }
};
</script>

<style scoped>
/* ========== ОСНОВНЫЕ СТИЛИ ========== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #333;
  padding: 20px;
}

/* ========== ШАПКА ========== */
.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 30px;
}

.header-title h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 10px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
  font-weight: 400;
}

.header-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 25px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 15px;
  color: white;
  min-width: 180px;
}

.stat-item:nth-child(2) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

/* ========== ПАНЕЛЬ УПРАВЛЕНИЯ ========== */
.control-panel {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 0 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.control-group {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.control-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.excel-btn {
  background: linear-gradient(135deg, #21d190 0%, #2bc48a 100%);
}

.summary-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.csv-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.refresh-btn {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.control-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.search-box {
  position: relative;
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 14px 20px 14px 50px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: #667eea;
}

/* ========== ФОРМА ========== */
.form-section, .table-section {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.section-header:hover {
  border-bottom-color: #667eea;
}

.section-header h2 {
  color: #333;
  font-size: 1.8rem;
  font-weight: 700;
}

.section-icon {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  transition: transform 0.3s ease;
}

.section-header:hover .section-icon {
  transform: scale(1.2);
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.5s ease;
  max-height: 1000px;
  overflow: hidden;
}

.slide-enter, .slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-20px);
}

.add-form {
  margin-top: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.required {
  color: #ff4757;
  font-size: 1.2rem;
}

.form-input {
  padding: 14px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

textarea.form-input {
  resize: vertical;
  min-height: 60px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.submit-btn {
  padding: 16px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.clear-btn {
  padding: 16px 32px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.submit-btn:hover, .clear-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* ========== ТАБЛИЦА ========== */
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 15px;
}

.table-header h2 {
  color: #333;
  font-size: 1.8rem;
  font-weight: 700;
}

.table-info {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  color: #666;
}

.table-container {
  overflow-x: auto;
  border-radius: 15px;
  border: 1px solid #e1e5e9;
  margin-bottom: 30px;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 1200px;
}

.table-header-cell {
  padding: 20px;
  text-align: left;
  font-weight: 700;
  color: #555;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 10;
}

.actions-header {
  min-width: 120px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.table-row {
  transition: all 0.2s ease;
}

.table-row:hover {
  background: linear-gradient(135deg, #f8fbff 0%, #eef6ff 100%);
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.table-cell {
  padding: 18px 20px;
  border-bottom: 1px solid #e1e5e9;
  color: #444;
  transition: all 0.3s ease;
}

.cell-content {
  display: inline-block;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.actions-cell {
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.table-row:hover .action-buttons {
  opacity: 1;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.edit-btn {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.delete-btn {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.empty-row {
  text-align: center;
}

.empty-cell {
  padding: 80px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  color: #888;
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.3;
}

.clear-search-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 15px;
}

/* ========== ИТОГОВАЯ СТРОКА ========== */
.table-footer {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.footer-label, .footer-total, .footer-empty, .footer-actions {
  padding: 20px;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
}

.footer-label {
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.footer-total {
  text-align: right;
  font-family: 'Courier New', monospace;
  font-weight: 700;
}

.footer-empty {
  text-align: center;
  opacity: 0.7;
}

/* ========== СТАТИСТИКА ========== */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
  margin-top: 30px;
}

.summary-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.4s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.summary-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 2.8rem;
  opacity: 0.9;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 0.9rem;
  font-weight: 600;
  opacity: 0.8;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-value {
  font-size: 2rem;
  font-weight: 800;
  font-family: 'Courier New', monospace;
  margin-bottom: 5px;
}

.card-unit {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

/* ========== ФУТЕР ========== */
.app-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 25px 30px;
  margin-top: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.copyright {
  font-size: 1rem;
  color: #666;
  font-weight: 500;
}

.footer-info {
  display: flex;
  gap: 30px;
  font-size: 0.9rem;
  color: #888;
}

/* ========== УВЕДОМЛЕНИЯ ========== */
.notification {
  position: fixed;
  top: 30px;
  right: 30px;
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 20px;
  z-index: 1000;
  min-width: 350px;
  animation: slideIn 0.5s ease;
  border-left: 5px solid;
}

.notification-success {
  border-left-color: #21d190;
}

.notification-error {
  border-left-color: #ff6b6b;
}

.notification-warning {
  border-left-color: #ffa502;
}

.notification-info {
  border-left-color: #4facfe;
}

.notification-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.notification-message {
  font-size: 0.9rem;
  color: #666;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.notification-close:hover {
  background: #f8f9fa;
  color: #333;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ========== АДАПТИВНОСТЬ ========== */
@media (max-width: 1200px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-stats {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 992px) {
  .control-panel {
    flex-direction: column;
    align-items: stretch;
  }
  
  .control-group {
    justify-content: center;
  }
  
  .search-box {
    width: 100%;
  }
  
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  #app {
    padding: 10px;
  }
  
  .app-header, .form-section, .table-section, .app-footer {
    padding: 20px;
  }
  
  .header-title h1 {
    font-size: 2rem;
  }
  
  .stat-item {
    min-width: 140px;
    padding: 12px 20px;
  }
  
  .control-btn {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .footer-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .footer-info {
    flex-direction: column;
    gap: 10px;
  }
  
  .notification {
    min-width: calc(100% - 60px);
    right: 30px;
    left: 30px;
  }
}

@media (max-width: 480px) {
  .header-stats {
    flex-direction: column;
  }
  
  .stat-item {
    width: 100%;
  }
  
  .control-group {
    flex-direction: column;
  }
  
  .control-btn {
    width: 100%;
    justify-content: center;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .submit-btn, .clear-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>