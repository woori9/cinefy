import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime';
import 'dayjs/locale/ko'

dayjs.extend(relativeTime);
dayjs.locale('ko')

const fromNow = (dateTime) => {
  const diff = dayjs().diff(dateTime,'days')

  if (diff < 1) return dayjs(dateTime).fromNow()
  return dayjs(dateTime).format("YYYY-MM-DD")
}
export default fromNow;
