import contactMapSVG from "../svg/contact-map.js";

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
    contactMapSVG('svg', document.getElementById('canvas').getContext('2d').data);
    let svg = document.getElementById('svg');
    let pre = '<?xml version="1.0" standalone="no"?>\r\n';
    let blob = new Blob([pre, svg.outerHTML], {type: 'image/svg+xml;charset=utf-8'});
    hl.href = URL.createObjectURL(blob);
    hl.setAttribute('download', 'you-name-it.svg');
    hl.click();
  });
}