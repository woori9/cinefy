<template>
  <div class="mini-modal">
    <!-- Mini Modal :video-id="'c2rgrqEFVKc'" -->
    <player
      :videoId="youtubevideoId"
      @endedVideo="nextVideo"
      :modaltype="'mini'"
    ></player>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Player from '@/components/utils/Player'
export default {
  name: 'MiniModal',
  components: {
    Player
  },
  data() {
    return {
      index: 0
    }
  },
  computed: {
    ...mapState([
      'movieOST',
    ]),
    youtubevideoId() {
      return this.movieOST[this.index]
    },
  },
  methods: {
    nextVideo() {
      this.index = (this.index + 1) % this.movieOST.length
    }
  },
}
</script>

<style>
.mini-modal {
  position: fixed;
  right: 0;
  bottom: 0;
  z-index: 99999;
}
</style>