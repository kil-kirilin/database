// src/components/ExcelExport.js
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

export const exportToExcel = (data, filename = 'export.xlsx') => {
  // Создаем новую книгу Excel
  const workbook = XLSX.utils.book_new();
  
  // Преобразуем данные в формат для Excel
  const worksheet = XLSX.utils.json_to_sheet(data);
  
  // Добавляем лист в книгу
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Данные');
  
  // Генерируем Excel файл
  const excelBuffer = XLSX.write(workbook, { 
    bookType: 'xlsx', 
    type: 'array' 
  });
  
  // Создаем Blob и сохраняем файл
  const dataBlob = new Blob([excelBuffer], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  });
  
  saveAs(dataBlob, filename);
};
