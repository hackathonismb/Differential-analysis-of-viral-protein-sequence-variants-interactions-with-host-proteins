import data from "./utils/sample-data.js"
import contactMapSVG from "./svg/contact-map.js";

window.onload = () => {
  contactMapSVG('svg-left', data);
  contactMapSVG('svg-right', data);
}