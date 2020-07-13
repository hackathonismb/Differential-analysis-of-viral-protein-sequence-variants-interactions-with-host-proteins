export default class BoxModel {
  constructor (w, h, opts={}) {
    this.margin = Object.assign({top: 0, right: 0, bottom: 0, left: 0}, opts.margin);
    this.padding = Object.assign({top: 0, right: 0, bottom: 0, left: 0}, opts.padding);
    this.borderWidth = opts.borderWidth ? opts.borderWidth : 0;
  }
}