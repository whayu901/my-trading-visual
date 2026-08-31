/**
 * Pasang grafik native di tab Dashboard.
 * Extensions > Apps Script > paste semua ini > Save > pilih buatGrafik > Run.
 * Aman dijalankan berkali-kali — grafik lama dihapus dulu.
 */
function buatGrafik() {
  const ss   = SpreadsheetApp.getActiveSpreadsheet();
  const dash = ss.getSheetByName('📊 Dashboard');
  const src  = ss.getSheetByName('📈 Data Chart');
  if (!dash || !src) {
    SpreadsheetApp.getUi().alert('Tab Dashboard atau Data Chart tidak ketemu.');
    return;
  }
  dash.getCharts().forEach(c => dash.removeChart(c));
  const buat = (type, ranges, row, col, judul, opts) => {
    let b = dash.newChart().setChartType(type);
    ranges.forEach(r => b = b.addRange(src.getRange(r)));
    b = b.setPosition(row, col, 0, 0)
         .setOption('title', judul).setOption('width', 460).setOption('height', 260)
         .setOption('titleTextStyle', {fontSize: 12, bold: true})
         .setOption('legend', {position: 'none'});
    for (const k in (opts || {})) b = b.setOption(k, opts[k]);
    dash.insertChart(b.build());
  };
  const CH = Charts.ChartType;
  buat(CH.LINE,   ['A4:B154'], 3,  8, 'Kurva Ekuitas — R kumulatif harian',
       {colors: ['#00bcd4'], pointSize: 3});
  buat(CH.COLUMN, ['D4:E154'], 17, 8, 'PnL Harian ($)', {colors: ['#1E3A8A']});
  buat(CH.BAR,    ['G4:G8', 'J4:J8'], 31, 8, 'Expectancy R per Tipe Setup', {colors: ['#065F46']});
  buat(CH.COLUMN, ['L4:M12'], 3,  16, 'Sebaran Hasil (R)', {colors: ['#7C2D12']});
  buat(CH.BAR,    ['O4:O10', 'Q4:Q10'], 17, 16, 'Expectancy R per Emosi', {colors: ['#831843']});
  buat(CH.PIE,    ['W4:X7'], 31, 16, 'Win / Loss / BE',
       {colors: ['#10B981', '#EF4444', '#9CA3AF'], legend: {position: 'right'}});
  ss.toast('6 grafik terpasang di Dashboard.', 'Selesai', 5);
}
