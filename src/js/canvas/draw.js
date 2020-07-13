import BoxModel from "../utils/box-model.js";
import {initializeCanvas} from "./setup.js";
import config from "../utils/config.js";

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
export function drawContactMap(canvas, data={x: [], y: [], data: {}}) {
  let w = config.gridWidth * data.x.length + config.margin.left + config.margin.right;
  let h = config.gridWidth * data.y.length + config.margin.top + config.margin.bottom;
  let ctx = initializeCanvas(canvas, {width: w, height: h});
  ctx.margin = config.margin;
  updateContactMap(ctx, data);
}

function updateContactMap(ctx, data, pos={x: 0, y: 0}) {
  ctx.save();
  ctx.clearRect(0, 0, ctx.w, ctx.h);
  ctx.translate(ctx.margin.left, ctx.margin.top);
  let w = config.gridWidth * data.x.length;
  let h = config.gridWidth * data.y.length;
  ctx.strokeStyle = config.lineColor;
  ctx.strokeWidth = config.lineWidth;
  ctx.strokeRect(0 - ctx.strokeWidth / 2, 0 - ctx.strokeWidth / 2, w, h);
  ctx.setLineDash([2, 6]);
  ctx.lineDashOffset = [-1, -1];
  ctx.lineCap = 'round';
  ctx.textBaseline = 'middle';
  ctx.textAlign = 'right';
  ctx.font = '16px monospace';
  // ctx.save();
  for (let i = 0; i < data.x.length; i++) {
    ctx.save();
    ctx.translate(config.gridWidth / 2 + i * config.gridWidth, 0);
    ctx.beginPath();
    ctx.moveTo(- ctx.strokeWidth / 2, 0);
    ctx.lineTo(- ctx.strokeWidth / 2, h);
    ctx.closePath();
    ctx.stroke();
    ctx.rotate(-(Math.PI / 2));
    ctx.fillText(data.x[i], 20, 0);
    ctx.restore();
  }
  for (let i = 0; i < data.y.length; i++) {
    ctx.beginPath();
    ctx.moveTo(0, config.gridWidth / 2 + i * config.gridWidth - ctx.strokeWidth / 2);
    ctx.lineTo(w, config.gridWidth / 2 + i * config.gridWidth - ctx.strokeWidth / 2);
    ctx.closePath();
    ctx.stroke();
    ctx.fillText(data.y[i], -10, config.gridWidth / 2 + i * config.gridWidth - ctx.strokeWidth / 2);
  }
  ctx.fillStyle = config.circleColor;
  for (let i = 0; i < data.x.length; i++) {
    for (let j = 0; j < data.y.length; j++) {
      if (data.data[`${data.x[i]}-${data.y[j]}`].value) {
        ctx.beginPath();
        ctx.arc(config.gridWidth / 2 + i * config.gridWidth, config.gridWidth / 2 + j * config.gridWidth, config.circleRadius,0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
  let x = pos.x - ctx.margin.left;

}