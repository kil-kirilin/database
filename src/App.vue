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
          <th>Действия</th> <!-- Добавим столбец для действий -->
        </tr>
      </thead>
      <tbody>
        <tr :key="column.name" v-for="column in columns">
          <td :key="index" v-for="(header, index) in headers">
            {{ column[header.name] }}
          </td>
          <td>
            <!-- Здесь можно будет добавить кнопки редактирования/удаления -->
            <button @click="deleteItem(column.number)" class="delete-button">Удалить</button>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <th scope="col"></th>
          <th scope="col">Итоговая сумма</th>
          <th scope="col">50</th>
          <th scope="col">24</th>
          <th scope="col">288</th>
          <th scope="col">46300</th>
          <th scope="col">555600</th>
          <th></th> <!-- Пустой столбец для действий -->
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
      newItem: { // Объект для хранения данных новой записи
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
      return this.headers.filter(header => header.name !== 'note');
    }
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get('http://localhost:5000/api/data');
        this.columns = response.data;
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
    async addItem() {
      try {
        // Убедимся, что числовые значения преобразуются в строки, если это необходимо для вашей БД
        const itemToSend = { ...this.newItem };
        for (const key in itemToSend) {
            if (itemToSend[key] !== null && typeof itemToSend[key] === 'number') {
                itemToSend[key] = String(itemToSend[key]);
            }
        }
        await axios.post('http://localhost:5000/api/data', itemToSend);
        this.fetchItems(); // Обновляем данные после добавления
        this.resetForm(); // Очищаем форму
      } catch (error) {
        console.error('Ошибка при добавлении элемента:', error);
      }
    },
    resetForm() {
      // Сбрасываем форму после успешного добавления
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
    },
    async deleteItem(itemNumber) {
      if (confirm(`Вы уверены, что хотите удалить элемент №${itemNumber}?`)) {
        try {
          await axios.delete(`http://localhost:5000/api/data/${itemNumber}`);
          this.fetchItems();
        } catch (error) {
          console.error('Ошибка при удалении элемента:', error);
        }
      }
    }
  },
  mounted() {
    this.fetchItems();
  }
};
</script>

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
  background-color: #4a90e2;
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
  border-top: 2px solid #4a90e2;
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
  background-color: #218838;
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