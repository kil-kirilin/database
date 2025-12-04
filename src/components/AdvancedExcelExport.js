// src/components/AdvancedExcelExport.js
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

export const exportToExcelWithStyles = (data, headers, filename = 'export.xlsx') => {
  // Создаем книгу
  const wb = XLSX.utils.book_new();
  
  // Создаем лист с данными
  const wsData = [
    // Заголовок
    ['Отчет по материалам', '', '', '', '', '', ''],
    [`Дата экспорта: ${new Date().toLocaleDateString('ru-RU')}`, '', '', '', '', '', ''],
    [], // Пустая строка
    
    // Заголовки таблицы
    headers.map(h => h.display),
    
    // Данные
    ...data.map(item => headers.map(h => item[h.name]))
  ];
  
  const ws = XLSX.utils.aoa_to_sheet(wsData);
  
  // Настраиваем ширину колонок
  const colWidths = headers.map(() => ({ wch: 15 }));
  ws['!cols'] = colWidths;
  
  // Объединяем ячейки для заголовка
  ws['!merges'] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: 6 } }, // Первая строка
    { s: { r: 1, c: 0 }, e: { r: 1, c: 6 } }  // Вторая строка
  ];
  
  // Добавляем лист в книгу
  XLSX.utils.book_append_sheet(wb, ws, 'Материалы');
  
  // Создаем лист с итогами
  const summaryWs = XLSX.utils.aoa_to_sheet([
    ['Сводная информация'],
    [],
    ['Показатель', 'Значение', 'Единица измерения'],
    ['Всего записей', data.length, 'шт'],
    ['Общая стоимость', '=СУММ(Материалы!G5:G100)', '₽'],
    ['Средняя цена за месяц', '=СРЗНАЧ(Материалы!F5:F100)', '₽']
  ]);
  
  XLSX.utils.book_append_sheet(wb, summaryWs, 'Итоги');
  
  // Сохраняем файл
  const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([wbout], { type: 'application/octet-stream' });
  saveAs(blob, filename);
};

// Экспорт в формате CSV
export const exportToCSV = (data, headers, filename = 'export.csv') => {
  const csvHeaders = headers.map(h => h.display).join(';');
  const csvRows = data.map(item => 
    headers.map(h => `"${item[h.name] || ''}"`).join(';')
  ).join('\n');
  
  const csvContent = `${csvHeaders}\n${csvRows}`;
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  saveAs(blob, filename);
};