<template>
  <div id="app">
    <header class="app-header">
      <h1>📦 Учет материалов 2025</h1>
      <p class="subtitle">Управление расходом материалов с автоматическим подсчетом</p>
    </header>

    <main class="app-main">
      <section class="form-section">
        <div class="section-header">
          <h2>Добавить материал</h2>
        </div>
        <form @submit.prevent="addItem" class="add-form">
          <div class="form-grid">
            <div class="form-group" v-for="header in headersWithoutIdAndNote" :key="header.name">
              <label :for="header.name">{{ header.display }}</label>
              <input 
                v-model="newItem[header.name]" 
                :id="header.name" 
                type="text" 
                :placeholder="`Введите ${header.display.toLowerCase()}`"
                class="form-input"
              />
            </div>
            <div class="form-group full-width">
              <label for="note">Примечание</label>
              <input 
                v-model="newItem.note" 
                id="note" 
                type="text" 
                placeholder="Дополнительная информация"
                class="form-input"
              />
            </div>
          </div>
          <button type="submit" class="submit-btn">
            <span class="btn-icon">✓</span>
            Добавить материал
          </button>
        </form>
      </section>

      <section class="table-section">
        <div class="section-header">
          <h2>Таблица расходов</h2>
        </div>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th v-for="header in headers" :key="header.name" class="table-header">
                  <span class="header-text">{{ header.display }}</span>
                </th>
                <th class="table-header">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="column in columns" :key="column.number" class="table-row">
                <td v-for="header in headers" :key="header.name" class="table-cell">
                  <span class="cell-content">{{ column[header.name] || '—' }}</span>
                </td>
                <td class="table-cell actions-cell">
                  <button @click="deleteItem(column.number)" class="delete-btn">
                    <span class="btn-icon">🗑️</span>
                    Удалить
                  </button>
                </td>
              </tr>
              <tr v-if="columns.length === 0" class="empty-row">
                <td :colspan="headers.length + 1" class="empty-cell">
                  <div class="empty-state">
                    <span class="empty-icon">📝</span>
                    <p>Нет данных. Добавьте первый материал.</p>
                  </div>
                </td>
              </tr>
            </tbody>
            <tfoot class="table-footer">
              <tr>
                <td class="footer-label">Итого</td>
                <td class="footer-total">—</td>
                <td v-for="(total, index) in totals" :key="index" class="footer-total">
                  {{ total.toLocaleString('ru-RU') }}
                </td>
                <td class="footer-empty"></td>
              </tr>
            </tfoot>
          </table>
        </div>
        
        <div class="summary-cards">
          <div class="summary-card" v-for="(summary, index) in summaryData" :key="index">
            <div class="card-icon">{{ summary.icon }}</div>
            <div class="card-content">
              <h3 class="card-title">{{ summary.title }}</h3>
              <p class="card-value">{{ summary.value.toLocaleString('ru-RU') }} {{ summary.unit }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="app-footer">
      <p>© 2025 Система учета материалов • Всего записей: {{ columns.length }}</p>
      <p class="timestamp" v-if="lastUpdate">Обновлено: {{ lastUpdate }}</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      headers: [
        { name: 'number', display: '№' },
        { name: 'name', display: 'Наименование' },
        { name: 'quantity', display: 'Кол-во' },
        { name: 'monthlyConsumption', display: 'Месяц' },
        { name: 'yearlyConsumption', display: 'Год' },
        { name: 'monthlyPrice', display: 'Цена/мес' },
        { name: 'yearlyPrice', display: 'Цена/год' },
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
      lastUpdate: null
    };
  },
  computed: {
    headersWithoutIdAndNote() {
      return this.headers.filter(header => header.name !== 'note');
    },
    totals() {
      return [
        this.totalQuantity,
        this.totalMonthlyConsumption,
        this.totalYearlyConsumption,
        this.totalMonthlyPrice,
        this.totalYearlyPrice
      ];
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
          value: this.totalYearlyPrice,
          unit: '₽'
        },
        {
          icon: '📈',
          title: 'Средний расход',
          value: this.columns.length > 0 ? this.totalMonthlyConsumption / this.columns.length : 0,
          unit: 'ед/мес'
        }
      ];
    }
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get('http://localhost:5000/api/data');
        this.columns = response.data;
        this.updateTimestamp();
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
    async addItem() {
      try {
        const itemToSend = { ...this.newItem };
        const numericFields = ['quantity', 'monthlyConsumption', 'yearlyConsumption', 'monthlyPrice', 'yearlyPrice'];
        
        for (let i = 0; i < numericFields.length; i++) {
          const field = numericFields[i];
          if (itemToSend[field]) {
            itemToSend[field] = parseFloat(itemToSend[field]) || 0;
          }
        }
        
        await axios.post('http://localhost:5000/api/data', itemToSend);
        this.fetchItems();
        this.resetForm();
      } catch (error) {
        console.error('Ошибка при добавлении элемента:', error);
      }
    },
    resetForm() {
      const fields = ['number', 'name', 'quantity', 'monthlyConsumption', 'yearlyConsumption', 'monthlyPrice', 'yearlyPrice', 'note'];
      for (let i = 0; i < fields.length; i++) {
        this.newItem[fields[i]] = '';
      }
    },
    async deleteItem(itemNumber) {
      if (confirm(`Удалить материал №${itemNumber}?`)) {
        try {
          await axios.delete(`http://localhost:5000/api/data/${itemNumber}`);
          this.fetchItems();
        } catch (error) {
          console.error('Ошибка при удалении элемента:', error);
        }
      }
    },
    updateTimestamp() {
      const now = new Date();
      this.lastUpdate = now.toLocaleTimeString('ru-RU', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      });
    }
  },
  mounted() {
    this.fetchItems();
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #333;
  padding: 20px;
}

.app-header {
  text-align: center;
  color: rgb(255, 255, 255);
  margin-bottom: 40px;
  padding: 20px;
}

.app-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  background: linear-gradient(45deg, #ffffff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  font-weight: 300;
}

.app-main {
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.section-header h2 {
  color: rgb(29, 1, 166);
  font-size: 1.8rem;
  font-weight: 600;
}

.section-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.form-section, .table-section {
  background: rgb(213, 243, 255);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
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

.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.form-input:focus {
  outline: none;
  border-color: #4a18ff;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.btn-icon {
  font-size: 1.2rem;
}

.table-container {
  overflow-x: auto;
  border-radius: 15px;
  border: 1px solid #e1e5e9;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.table-header {
  padding: 18px 20px;
  text-align: left;
  font-weight: 600;
  color: #555;
  background: #f8f9fa;
  border-bottom: 2px solid #e1e5e9;
  white-space: nowrap;
}

.header-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.table-row {
  transition: all 0.2s ease;
}

.table-row:hover {
  background: #f0f4ff;
}

.table-cell {
  padding: 16px 20px;
  border-bottom: 1px solid #e1e5e9;
  color: #444;
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

.delete-btn {
  padding: 8px 16px;
  background: linear-gradient(135deg, #a50000 0%, #ff0d00 100%);
  color: white;
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

.delete-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
}

.empty-row {
  text-align: center;
}

.empty-cell {
  padding: 60px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  color: #598aee;
}

.empty-icon {
  font-size: 3rem;
  opacity: 0.5;
}

.table-footer {
  background: linear-gradient(135deg, #667eea 0%, #74eaff 100%);
}

.footer-label, .footer-total, .footer-empty {
  padding: 20px;
  color: rgb(255, 255, 255);
  font-weight: 600;
  font-size: 1.1rem;
}

.footer-total {
  text-align: right;
  font-family: 'Courier New', monospace;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.summary-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 15px;
  padding: 25px;
  color: white;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.summary-card:nth-child(2) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.summary-card:nth-child(3) {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.card-icon {
  font-size: 2.5rem;
  opacity: 0.9;
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 0.9rem;
  font-weight: 500;
  opacity: 0.9;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-value {
  font-size: 1.8rem;
  font-weight: 700;
  font-family: 'Courier New', monospace;
}

.app-footer {
  text-align: center;
  color: white;
  padding: 20px;
  margin-top: 40px;
  opacity: 0.8;
  font-size: 0.9rem;
}

.timestamp {
  margin-top: 5px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .app-header h1 {
    font-size: 2rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-cards {
    grid-template-columns: 1fr;
  }
  
  .table-container {
    font-size: 0.9rem;
  }
  
  .table-cell, .table-header {
    padding: 12px 15px;
  }
}

@media (max-width: 480px) {
  #app {
    padding: 10px;
  }
  
  .form-section, .table-section {
    padding: 20px;
  }
  
  .section-header h2 {
    font-size: 1.5rem;
  }
}
</style>