import axios from 'axios';

const API = axios.create({ baseURL: '/api' });

export const getWeather    = (district) => API.get(`/data/weather/${district}`);
export const getMarket     = ()          => API.get('/data/market');
export const getAdvisory   = (season)    => API.get(`/data/advisory?season=${season}`);
export const getSchemes    = ()          => API.get('/data/schemes');
export const getDistricts  = ()          => API.get('/data/districts');
export const previewReport = (data)      => API.post('/report/preview', data);
export const generateReport = (data)     => API.post('/report/generate', data, { responseType: 'blob' });
export const sendChat      = (message, history) => API.post('/chat/message', { message, history });

export default API;
