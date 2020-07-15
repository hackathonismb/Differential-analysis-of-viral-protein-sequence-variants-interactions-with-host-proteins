const base = '../figures/';
const imageNames = [
  "6M0J_all_contacts.png",
  "6M0J_contact.png",
  "2AJF_all_contacts.png",
  "6M0J_H-Bonds.png",
  "Team 2A.png",
  "Contact2.png",
  "2AJF_H-Bonds.png",
  "Contact1.png",
  "Contact_Combined.png",
  "2AJF_contact.png",
].sort();

export default function setupImgSliding() {
  let c = document.getElementById('gallery-image');
  let dw = document.getElementById('dots-wrapper');

  for (let i = 0; i < imageNames.length; i++) {
    let d = dw.appendChild(document.createElement('div'));
    d.classList.add('dot');
    let img = c.appendChild(document.createElement('img'));
    img.classList.add('image');
    img.setAttribute('src', base + imageNames[i]);
    if (i === 0) {
      d.classList.add('active');
      img.classList.add('current');
    } else {
      img.classList.add('upcoming');
    }
  }

  let cur = 0;
  let images = c.getElementsByClassName('image');
  let dots = dw.getElementsByClassName('dot');

  let toLeft = document.getElementById('to-left');
  let toRight = document.getElementById('to-right');
  
  toLeft.addEventListener('click', () => {
    if (cur > 0) {
      images[cur].classList.remove('current');
      images[cur].classList.add('upcoming');
      dots[cur].classList.remove('active');
      cur--;
      images[cur].classList.remove('gone');
      images[cur].classList.add('current');
      dots[cur].classList.add('active');
    }
  });
  toRight.addEventListener('click', () => {
    if (cur < images.length - 1) {
      images[cur].classList.remove('current');
      images[cur].classList.add('gone');
      dots[cur].classList.remove('active');
      cur++;
      images[cur].classList.remove('upcoming');
      images[cur].classList.add('current');
      dots[cur].classList.add('active');
    }
  });

  for (let i = 0; i < dots.length; i++) {
    dots[i].addEventListener('click', function () {
      cur = i;
      images[i].classList.add('current');
      images[i].classList.remove('gone', 'upcoming');
      dots[i].classList.add('active');
      for (let j = 0; j < i; j++) {
        images[j].classList.remove('current', 'upcoming');
        images[j].classList.add('gone');
        dots[j].classList.remove('active');
      }
      for (let k = i + 1; k < dots.length; k++) {
        images[k].classList.remove('current', 'gone');
        images[k].classList.add('upcoming');
        dots[k].classList.remove('active');
      }
    });
  }
}