export function initializeCanvas(canvas, opts={}) {
  let ctx = null;
  try {
    ctx = canvas.getContext("2d");
  } catch (err) {
    throw err;
  }
  if (!ctx) {
    throw "canvas is not supported in the browser";
  }

  ctx.opts = Object.assign({}, {width: canvas.clientWidth, height: canvas.clientHeight}, opts);
  canvas.style.width = ctx.opts.width + 'px';
  canvas.style.height = ctx.opts.height + 'px';

  ctx.w = ctx.opts.width;
  ctx.h = ctx.opts.height;

  ctx.devicePixelRatio = window.devicePixelRatio;
  if (ctx.devicePixelRatio < 1) {
    ctx.devicePixelRatio = 1;
  }

  canvas.width = ctx.devicePixelRatio * ctx.opts.width;
  canvas.height = ctx.devicePixelRatio * ctx.opts.height;
  ctx.scale(ctx.devicePixelRatio, ctx.devicePixelRatio);

  return ctx;
}

export function setupScale(ctx) {
  ctx.w = ctx.canvas.clientWidth;
  ctx.h = ctx.canvas.clientHeight;
  ctx.devicePixelRatio = window.devicePixelRatio;
  ctx.canvas.width = ctx.w * ctx.devicePixelRatio;
  ctx.canvas.height = ctx.h * ctx.devicePixelRatio;
  ctx.scale(ctx.devicePixelRatio, ctx.devicePixelRatio);
}