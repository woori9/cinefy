import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.VUE_APP_YOUTUBE_API_URL,
  params: {
    key: process.env.VUE_APP_YOUTUBE_API_KEY,
    part: 'snippet',
    type: 'video',
  },
});

export default instance;
