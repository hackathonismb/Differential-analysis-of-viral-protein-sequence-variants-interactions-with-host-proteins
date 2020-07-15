export default function setupDownload() {
  document.getElementById('save-as-jpg').addEventListener('click', function() {;
    this.href = document.getElementById('canvas').toDataURL('image/jpeg', 1.0);
  });
  document.getElementById('save-as-png').addEventListener('click', function() {
    this.href = document.getElementById('canvas').toDataURL();
  });
  document.getElementById('save-as-svg').addEventListener('click', function() {

  });
}