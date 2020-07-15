export default function contactMapSVG(data={x: [], y: [], data: {}}) {
  let svg = document.getElementById('svg');
  while (svg.lastChild) {
    svg.removeChild(svg.lastChild);
  }
  let canvas = document.getElementById('canvas');
  svg.setAttribute('width', canvas.clientWidth + '');
  svg.setAttribute('height', canvas.clientHeight + '');
  const xmlns = "http://www.w3.org/2000/svg";
  let g = svg.appendChild(document.createElementNS(xmlns, 'g'));
  
}