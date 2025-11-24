<template>
  <div id="app">
  <table>
    <caption>
      Таблица расхода материала за 2025 год
    </caption>
  <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Наименование</th>
      <th scope="col">Колличество</th>
      <th scope="col">Расход за месяц</th>
      <th scope="col">Расход за год</th>
      <th scope="col">Цена за месяц (руб)</th>
      <th scope="col">Цена за год (руб)</th>
      <th scope="col">Примечание</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Гипс</td>
      <td>15 кг</td>
      <td>3 кг</td>
      <td>36 кг</td>
      <td>990</td>
      <td>11880</td>
    </tr>
  </tbody>
 <tbody>
    <tr>
      <td>2</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>3</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="col"> </th>
      <th scope="col">Итоговая сумма</th>
      <th scope="col">50</th>
      <th scope="col">24</th>
      <th scope="col">288</th>
      <th scope="col">46300</th>
      <th scope="col">555600</th>
    </tr>
  </tfoot>
</table>
</div>
</template>

<script>

export default {
  name: 'App',
  components: {
  }
}
</script>

<style>
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
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  font-size: 16px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
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
  border-right: 1px solid rgba(255,255,255,0.3);
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
</style>
