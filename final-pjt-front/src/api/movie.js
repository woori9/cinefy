import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
  params: {
    api_key: process.env.VUE_APP_API_KEY,
  },
});

export default instance;
