import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

import aeHandler from './api/aliexpress.js';
import mlHandler from './api/mercadolibre.js';

// Mock request and response
const reqAE = { query: { q: 'humidificador' } };
const resAE = {
  setHeader: () => {},
  status: (code) => ({
    json: (data) => console.log('AE Error JSON:', data)
  }),
  json: (data) => {
    console.log('--- AliExpress Results ---');
    console.log(`Found ${data.products?.length || 0} products.`);
    if(data.products && data.products.length > 0) {
      console.log('Top product:', data.products[0]);
    }
  }
};

const reqML = { query: { q: 'humidificador' } };
const resML = {
  setHeader: () => {},
  status: (code) => ({
    json: (data) => console.log('ML Error JSON:', data)
  }),
  json: (data) => {
    console.log('--- MercadoLibre Results ---');
    console.log(`Avg Price: $${data.average_price_ars} ARS`);
    if(data.products && data.products.length > 0) {
      console.log('Top listing:', data.products[0].title, '- $', data.products[0].price);
    }
  }
};

async function test() {
  await aeHandler(reqAE, resAE);
  await mlHandler(reqML, resML);
}

test();
