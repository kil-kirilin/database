<template>
  <div id="app">
    <h1>Добавить новый материал</h1>
    <form @submit.prevent="addItem" class="add-item-form">
      <div class="form-group" v-for="header in headersWithoutIdAndNote" :key="header.name">
        <label :for="header.name">{{ header.display }}:</label>
        <input v-model="newItem[header.name]" :id="header.name" type="text" required />
      </div>
      <div class="form-group">
        <label for="note">Примечание:</label>
        <input v-model="newItem.note" id="note" type="text" />
      </div>
      <button type="submit">Добавить</button>
    </form>

    <br /><br />

    <table>
      <caption>
        Таблица расхода материала за 2025 год
      </caption>
      <thead>
        <tr>
          <th :key="header.display" v-for="header in headers">{{ header.display }}</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr :key="column.number" v-for="column in columns">
          <td :key="header.name" v-for="header in headers">
            {{ column[header.name] }}
          </td>
          <td>
            <button @click="deleteItem(column.number)" class="delete-button">Удалить</button>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <th scope="col"></th>
          <th scope="col">Итоговая сумма</th>
          <th scope="col">{{ totalQuantity }}</th>
          <th scope="col">{{ totalMonthlyConsumption }}</th>
          <th scope="col">{{ totalYearlyConsumption }}</th>
          <th scope="col">{{ totalMonthlyPrice }}</th>
          <th scope="col">{{ totalYearlyPrice }}</th>
          <th></th>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    console.log('Инициализация компонента App');
    return {
      headers: [
        { name: 'number', display: '№' },
        { name: 'name', display: 'Наименование' },
        { name: 'quantity', display: 'Колличество' },
        { name: 'monthlyConsumption', display: 'Расход за месяц' },
        { name: 'yearlyConsumption', display: 'Расход за год' },
        { name: 'monthlyPrice', display: 'Цена за месяц (руб)' },
        { name: 'yearlyPrice', display: 'Цена за год (руб)' },
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
      }
    };
  },
  computed: {
    // Вычисляемое свойство, чтобы не отображать 'note' в обязательных полях формы
    headersWithoutIdAndNote() {
      console.log('Вычисление headersWithoutIdAndNote');
      const filteredHeaders = [];
      
      for (var i = 0; i < this.headers.length; i++) {
        var header = this.headers[i];
        console.log(`Проверка заголовка: ${header.name} - ${header.display}`);
        
        if (header.name !== 'note') {
          filteredHeaders.push(header);
          console.log(`Добавлен заголовок: ${header.name}`);
        }
      }
      
      console.log('Итоговые заголовки без note:', filteredHeaders);
      return filteredHeaders;
    },
    
    // Вычисляемые свойства для итоговых сумм с использованием классического цикла for
    totalQuantity() {
      console.log('Вычисление totalQuantity');
      var sum = 0;
      
      for (var i = 0; i < this.columns.length; i++) {
        var item = this.columns[i];
        var value = parseFloat(item.quantity) || 0;
        console.log(`Элемент ${i + 1}: quantity = ${item.quantity}, преобразовано в: ${value}`);
        sum += value;
        console.log(`Текущая сумма: ${sum}`);
      }
      
      console.log(`Итоговая сумма quantity: ${sum}`);
      return sum;
    },
    
    totalMonthlyConsumption() {
      console.log('Вычисление totalMonthlyConsumption');
      var sum = 0;
      
      for (var i = 0; i < this.columns.length; i++) {
        var item = this.columns[i];
        var value = parseFloat(item.monthlyConsumption) || 0;
        console.log(`Элемент ${i + 1}: monthlyConsumption = ${item.monthlyConsumption}, преобразовано в: ${value}`);
        sum += value;
        console.log(`Текущая сумма: ${sum}`);
      }
      
      console.log(`Итоговая сумма monthlyConsumption: ${sum}`);
      return sum;
    },
    
    totalYearlyConsumption() {
      console.log('Вычисление totalYearlyConsumption');
      var sum = 0;
      
      for (var i = 0; i < this.columns.length; i++) {
        var item = this.columns[i];
        var value = parseFloat(item.yearlyConsumption) || 0;
        console.log(`Элемент ${i + 1}: yearlyConsumption = ${item.yearlyConsumption}, преобразовано в: ${value}`);
        sum += value;
        console.log(`Текущая сумма: ${sum}`);
      }
      
      console.log(`Итоговая сумма yearlyConsumption: ${sum}`);
      return sum;
    },
    
    totalMonthlyPrice() {
      console.log('Вычисление totalMonthlyPrice');
      var sum = 0;
      
      for (var i = 0; i < this.columns.length; i++) {
        var item = this.columns[i];
        var value = parseFloat(item.monthlyPrice) || 0;
        console.log(`Элемент ${i + 1}: monthlyPrice = ${item.monthlyPrice}, преобразовано в: ${value}`);
        sum += value;
        console.log(`Текущая сумма: ${sum}`);
      }
      
      console.log(`Итоговая сумма monthlyPrice: ${sum}`);
      return sum;
    },
    
    totalYearlyPrice() {
      console.log('Вычисление totalYearlyPrice');
      var sum = 0;
      
      for (var i = 0; i < this.columns.length; i++) {
        var item = this.columns[i];
        var value = parseFloat(item.yearlyPrice) || 0;
        console.log(`Элемент ${i + 1}: yearlyPrice = ${item.yearlyPrice}, преобразовано в: ${value}`);
        sum += value;
        console.log(`Текущая сумма: ${sum}`);
      }
      
      console.log(`Итоговая сумма yearlyPrice: ${sum}`);
      return sum;
    }
  },
  methods: {
    async fetchItems() {
      console.log('Начало загрузки данных...');
      try {
        const response = await axios.get('http://localhost:5000/api/data');
        console.log('Данные успешно получены:', response.data);
        this.columns = response.data;
        console.log('Количество загруженных элементов:', this.columns.length);
        
        // Логируем все элементы для отладки
        for (var i = 0; i < this.columns.length; i++) {
          var item = this.columns[i];
          console.log(`Элемент ${i + 1}:`, item);
        }
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
        console.error('Детали ошибки:', error.response ? error.response.data : 'Нет ответа от сервера');
      }
    },
    
    async addItem() {
      console.log('Добавление нового элемента...');
      console.log('Данные для отправки:', this.newItem);
      
      try {
        // Преобразуем числовые поля перед отправкой
        const itemToSend = { ...this.newItem };
        console.log('Копия данных перед преобразованием:', itemToSend);
        
        // Преобразуем строки в числа для вычислений на сервере
        const numericFields = ['quantity', 'monthlyConsumption', 'yearlyConsumption', 'monthlyPrice', 'yearlyPrice'];
        
        for (var i = 0; i < numericFields.length; i++) {
          var field = numericFields[i];
          if (itemToSend[field]) {
            var originalValue = itemToSend[field];
            itemToSend[field] = parseFloat(itemToSend[field]) || 0;
            console.log(`Преобразование поля ${field}: "${originalValue}" -> ${itemToSend[field]}`);
          }
        }
        
        console.log('Данные после преобразования для отправки:', itemToSend);
        
        await axios.post('http://localhost:5000/api/data', itemToSend);
        console.log('Элемент успешно добавлен на сервер');
        
        this.fetchItems(); // Обновляем данные после добавления
        this.resetForm(); // Очищаем форму
        
        console.log('Форма сброшена, данные обновлены');
      } catch (error) {
        console.error('Ошибка при добавлении элемента:', error);
        console.error('Детали ошибки:', error.response ? error.response.data : 'Нет ответа от сервера');
      }
    },
    
    resetForm() {
      console.log('Сброс формы...');
      // Используем классический цикл for для сброса всех полей формы
      const fields = ['number', 'name', 'quantity', 'monthlyConsumption', 'yearlyConsumption', 'monthlyPrice', 'yearlyPrice', 'note'];
      
      for (var i = 0; i < fields.length; i++) {
        var field = fields[i];
        console.log(`Сброс поля ${field}: "${this.newItem[field]}" -> ""`);
        this.newItem[field] = '';
      }
      
      console.log('Форма сброшена:', this.newItem);
    },
    
    async deleteItem(itemNumber) {
      console.log(`Попытка удаления элемента №${itemNumber}`);
      if (confirm(`Вы уверены, что хотите удалить элемент №${itemNumber}?`)) {
        try {
          console.log(`Отправка запроса на удаление элемента №${itemNumber}`);
          await axios.delete(`http://localhost:5000/api/data/${itemNumber}`);
          console.log(`Элемент №${itemNumber} успешно удален`);
          this.fetchItems();
        } catch (error) {
          console.error('Ошибка при удалении элемента:', error);
          console.error('Детали ошибки:', error.response ? error.response.data : 'Нет ответа от сервера');
        }
      } else {
        console.log('Удаление отменено пользователем');
      }
    }
  },
  
  mounted() {
    console.log('Компонент смонтирован, начинаем загрузку данных');
    this.fetchItems();
  },
  
  watch: {
    // Наблюдаем за изменениями в данных для отладки
    columns: {
      handler(newVal) {
        console.log('Данные таблицы изменены:', newVal);
        console.log('Количество элементов:', newVal.length);
      },
      deep: true
    },
    
    // Наблюдаем за изменениями в итоговых суммах
    totalQuantity(newVal) {
      console.log('totalQuantity изменилось:', newVal);
    },
    
    totalMonthlyPrice(newVal) {
      console.log('totalMonthlyPrice изменилось:', newVal);
    },
    
    totalYearlyPrice(newVal) {
      console.log('totalYearlyPrice изменилось:', newVal);
    }
  }
};
</script>

<style scoped>
/* Стили остаются без изменений */
.add-item-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  grid-column: span 2;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #45a049;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

.delete-button {
  padding: 5px 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #d32f2f;
}

tfoot tr {
  background-color: #e8f5e8;
  font-weight: bold;
}

tfoot th:nth-child(n+3):nth-child(-n+7) {
  text-align: right;
  font-weight: bold;
}
</style>

<style scoped>
/* Стили остаются без изменений */
.add-item-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  grid-column: span 2;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #45a049;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

.delete-button {
  padding: 5px 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #d32f2f;
}

tfoot tr {
  background-color: #e8f5e8;
  font-weight: bold;
}

tfoot th:nth-child(n+3):nth-child(-n+7) {
  text-align: right;
  font-weight: bold;
}
</style>

<style scoped>
/* Опционально: добавьте форматирование для чисел */
tfoot th:nth-child(n+3):nth-child(-n+7) {
  text-align: right;
  font-weight: bold;
}
</style>

<style>
/* Ваши существующие стили */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
table {
  width: 90%;
  margin: 0 auto;
  border-collapse: collapse;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 20px; /* Отступ от формы */
}
caption {
  caption-side: top;
  margin-bottom: 15px;
  font-size: 1.5em;
  font-weight: 600;
  color: #2c3e50;
}
thead {
  background-color: #1ccefb;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
thead th {
  padding: 12px 15px;
  border-right: 1px solid rgba(255, 255, 255, 0.3);
}
thead th:last-child {
  border-right: none;
}
tbody tr:nth-child(even) {
  background-color: #f4f7fc;
}
tbody td {
  padding: 12px 15px;
  border-bottom: 1px solid #e1e8f0;
  color: #333;
  text-align: center;
}
tbody td:first-child,
tbody td:nth-child(2) {
  text-align: left;
  padding-left: 20px;
}
tbody tr:hover {
  background-color: #dbeeff;
  cursor: pointer;
}
tfoot {
  background-color: #eaf1fb;
  font-weight: 600;
  color: #2c3e50;
}
tfoot th {
  padding: 12px 15px;
  border-top: 2px solid #48dffa;
  text-align: center;
}
tfoot th:first-child {
  text-align: left;
  padding-left: 20px;
}

/* Стили для новой формы */
.add-item-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  max-width: 90%;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.form-group label {
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}

.add-item-form button {
  grid-column: 1 / -1; /* Кнопка занимает всю ширину */
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.2s ease-in-out;
}

.add-item-form button:hover {
  background-color: #01beee;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s ease-in-out;
}

.delete-button:hover {
  background-color: #c82333;
}
</style>