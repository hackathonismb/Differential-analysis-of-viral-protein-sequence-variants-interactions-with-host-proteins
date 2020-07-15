import drawContactMap from "./canvas/contact-map.js";
import data from "./utils/sample-data.js";
import setupDownload from "./utils/download.js";
import setupImgSliding from "./utils/image-sliding.js";

window.onload = () => {
  drawContactMap(document.getElementById('canvas'), data);
  handleModeSwitch();
  handleTabSwitch();
  setupDownload();
  setupImgSliding();
};

function handleTabSwitch() {
  let sw = document.getElementsByClassName('switch-controller')[0];
  for (let ctrl of document.getElementsByClassName('switcher')) {
    ctrl.addEventListener('click', function() {
      sw.classList.toggle('contact');
      sw.classList.toggle('network');
    });
  }
}

function handleModeSwitch() {
  let main = document.getElementsByClassName('main')[0];
  let live = document.getElementById('live');
  let gallery = document.getElementById('gallery');
  live.addEventListener('click', () => {
    main.classList.add('live');
    main.classList.remove('gallery');
  });
  gallery.addEventListener('click', () => {
    main.classList.remove('live');
    main.classList.add('gallery');
  });
}