import {initializeCanvas} from "./setup.js";
import config from "../utils/config.js";
import colors from "../utils/colors.js";

let getColor = colors();

/**
 * draw contact map
 * @param canvas
 * @param data, i.e. {
 *   x: ['a', 'b', 'c'],
 *   y: ['d', 'e', 'f'],
 *   data: {
 *     'a-d': {type: '', value: 1},
 *     'a-e': {type: '', value: 1},
 *     'a-f': {type: '', value: 1},
 *     ...
 *   }
 * }
 */
export default function drawContactMap(canvas, data = {x: [], y: [], data: {}}) {
  let gridWidth = config.gridWidth;
  // the size of the grid plus margins
  let w = gridWidth * (data.x.length + 1) + config.margin.left + config.margin.right;
  let h = gridWidth * (data.y.length + 1) + config.margin.top + config.margin.bottom;
  let ctx = initializeCanvas(canvas, {width: w, height: h});
  ctx.data = data;
  ctx.highlighted = false;

  canvas.infoPanel = document.getElementById('info-panel');

  requestAnimationFrame(() => {
    updateContactMap(ctx, true);
  });

  canvas.addEventListener('contextmenu', evt => {
    evt.preventDefault();
    let rect = canvas.getBoundingClientRect();
    let x = evt.clientX - rect.left - config.margin.left + config.lineWidth / 2;
    let y = evt.clientY - rect.top - config.margin.top + config.lineWidth / 2;
    let m = getIndex(x, w, gridWidth, config.circleRadius);
    let n = getIndex(y, h, gridWidth, config.circleRadius);
    let obj = data.data[`${data.x[m]}-${data.y[n]}`];
    ctx.highlighted = m > -1 && n > -1 && obj.value;
    if (ctx.highlighted) {
      canvas.infoPanel.classList.add('live');
      updateInfoPanel(canvas.infoPanel, obj, {left: evt.clientX, top: evt.clientY});
    }
  });

  canvas.addEventListener('mouseover', evt => {
    let rect = canvas.getBoundingClientRect();
    requestAnimationFrame(() => {
      updateContactMap(ctx, false, {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top,
      });
      canvas.infoPanel.classList.remove('live');
    })
  });
  canvas.addEventListener('mousemove', evt => {
    let rect = canvas.getBoundingClientRect();
    requestAnimationFrame(() => {
      updateContactMap(ctx, true, {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top,
      });
      canvas.infoPanel.classList.remove('live');
    })
  });
  canvas.addEventListener('mouseleave', () => {
    requestAnimationFrame(() => {
      updateContactMap(ctx, false);
      canvas.infoPanel.classList.remove('live');
    });
  });
}

function updateContactMap(ctx, required, pos = {x: 0, y: 0}) {
  let data = ctx.data;

  let gridWidth = config.gridWidth;
  // the real size of the grid
  let w = gridWidth * (data.x.length + 1);
  let h = gridWidth * (data.y.length + 1);

  let x = pos.x - config.margin.left + config.lineWidth / 2;
  let y = pos.y - config.margin.top + config.lineWidth / 2;
  let m = getIndex(x, w, gridWidth, config.circleRadius);
  let n = getIndex(y, h, gridWidth, config.circleRadius);
  ctx.highlighted = m > -1 && n > -1 && data.data[`${data.x[m]}-${data.y[n]}`].value;

  if (!ctx.highlighted && !required) {
    return;
  }

  ctx.save();
  ctx.clearRect(0, 0, ctx.w, ctx.h);

  ctx.strokeStyle = config.lineColor;
  ctx.translate(config.margin.left - config.lineWidth / 2, config.margin.top - config.lineWidth / 2);
  ctx.strokeRect(0, 0, w, h);

  ctx.setLineDash(config.lineDash);
  ctx.lineDashOffset = [0, 0];
  ctx.lineCap = 'butt';
  ctx.textBaseline = 'middle';
  ctx.font = config.font;
  ctx.fillStyle = config.textColor;

  // ctx.save();
  for (let i = 0; i < data.x.length; i++) {
    ctx.save();
    if (ctx.highlighted && i === m) {
      ctx.fillStyle = config.textHighlightColor;
      ctx.strokeStyle = config.lineHighlightColor;
    } else {
      ctx.fillStyle = config.textColor;
      ctx.strokeStyle = config.lineColor;
    }
    ctx.translate((i + 1) * gridWidth, 0);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, h);
    ctx.closePath();
    ctx.stroke();
    ctx.rotate(-(Math.PI / 2));
    ctx.textAlign = 'left';
    ctx.fillText(data.x[i], config.textMargin, 0);
    ctx.restore();
  }
  for (let i = 0; i < data.y.length; i++) {
    if (ctx.highlighted && i === n) {
      ctx.fillStyle = config.textHighlightColor;
      ctx.strokeStyle = config.lineHighlightColor;
    } else {
      ctx.fillStyle = config.textColor;
      ctx.strokeStyle = config.lineColor;
    }
    ctx.beginPath();
    ctx.moveTo(0, (i + 1) * gridWidth);
    ctx.lineTo(w, (i + 1) * gridWidth);
    ctx.closePath();
    ctx.stroke();
    ctx.textAlign = 'right';
    ctx.fillText(data.y[i], -config.textMargin, (i + 1) * gridWidth);
  }
  ctx.fillStyle = config.circleColor;
  for (let i = 0; i < data.x.length; i++) {
    for (let j = 0; j < data.y.length; j++) {
      let obj = data.data[`${data.x[i]}-${data.y[j]}`];
      if (obj.value) {
        if (ctx.highlighted && i === m && j === n) {
          ctx.fillStyle = getColor(obj.type, true);
          ctx.shadowColor = ctx.fillStyle;
          ctx.shadowBlur = 8;
        } else {
          ctx.fillStyle = getColor(obj.type, false);
        }
        ctx.beginPath();
        ctx.arc((i + 1) * gridWidth, (j + 1) * gridWidth, config.circleRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }
  }

  ctx.restore();
}

function getIndex(d, max, unit, r) {
  if (d < (unit - r) || d > (max - unit + r)) {
    return -1;
  }
  let x1 = d - d % unit;
  let x2 = x1 + unit;
  if (d - x1 < r) {
    return x1 / unit - 1;
  }
  if (x2 - d < r) {
    return x2 / unit - 1;
  }
  return -1;
}

function updateInfoPanel(panel, obj, pos = {top: 0, left: 0}) {
  panel.style.top = `${pos.top}px`;
  panel.style.left = `${pos.left}px`;
  let spans = panel.getElementsByClassName('value');
  let values = [obj.x, obj.y, obj.type, obj.value];
  let i = 0;
  for (let span of spans) {
    span.innerText = `${values[i++]}`;
  }
}