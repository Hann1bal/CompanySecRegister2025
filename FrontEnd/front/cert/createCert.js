// cert.js
const devcert = require("devcert");

async function getCert() {
  const { key, cert } = await devcert.certificateFor("localhost");
  return { key, cert };
}

module.exports = { getCert };
