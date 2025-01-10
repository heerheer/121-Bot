// encrypt.js
const { RSAUtils, BigInt } = require('./security');
// 获取命令行参数
const args = process.argv.slice(2);
const dataToEncrypt = args[0];

RSAUtils.setMaxDigits(131);
var key = RSAUtils.getKeyPair("010001", '', "008aed7e057fe8f14c73550b0e6467b023616ddc8fa91846d2613cdb7f7621e3cada4cd5d812d627af6b87727ade4e26d26208b7326815941492b2204c3167ab2d53df1e3a2c9153bdb7c8c2e968df97a5e7e01cc410f92c4c2c2fba529b3ee988ebc1fca99ff5119e036d732c368acf8beba01aa2fdafa45b21e4de4928d0d403");
var result = RSAUtils.encryptedString(key, dataToEncrypt);
console.log(result);