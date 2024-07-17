// const CryptoJS = require('crypto-js');

// function encrypt(message, key) {
//   const iv = CryptoJS.lib.WordArray.random(16);
//   const encrypted = CryptoJS.AES.encrypt(message, key, { iv: iv });
//   return {
//     iv: iv.toString(),
//     encrypted: encrypted.toString()
//   };
// }

// // Example usage
// const message = 'This is a secret message';
// const key = 'your_secret_key'; // Replace with a strong, random key

// const encryptedData = encrypt(message, key);
// console.log(encryptedData);