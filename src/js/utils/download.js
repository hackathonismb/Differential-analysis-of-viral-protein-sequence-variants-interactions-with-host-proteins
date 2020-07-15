export default function setupDownload() {
  let hl = document.getElementById('download-handler');
  document.getElementById('save-as-jpg').addEventListener('click', function() {
    hl.href = document.getElementById('canvas').toDataURL('image/jpeg', 1.0);
    hl.setAttribute('download', 'you-name-it.jpg');
    hl.click();
  });
  document.getElementById('save-as-png').addEventListener('click', function() {
    hl.href = document.getElementById('canvas').toDataURL();
    hl.setAttribute('download', 'you-name-it.png');
    hl.click();
  });
  document.getElementById('save-as-svg').addEventListener('click', function() {

  });
}