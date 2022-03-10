<template>
  <div :class="{ box : divBox }">
    <youtube :class="`size-${modaltype}`"
      :video-id="videoId"
      :player-vars="playerVars"
      ref="youtube"
      @ready="ready"
      @playing="playing"
      @ended="ended"
      @error="error"
    />
  </div>
</template>

<script>

export default {
  name: 'Player',
  data() {
    return {
      index: -1
    }
  },
  props: {
    videoId: {
      type: String
    },
    modaltype: {
      type: String
    }
  },
  methods: {
    ready(){
      console.log('ready')
    },
    playing(){
      console.log('playing')
    },
    ended(){
      console.log('ended')
      this.$emit('endedVideo')
    },
    error(){
      console.log('error')
    }
  },
  computed: {
    divBox() {
      return this.modaltype === "default"
    },
    playerVars() {
      return {
        player3: Object,
        rel: 0,
        autoplay: 1,
        enablejsapi: 1,
        fs: 0,
        playsinline: 1,
        ivLoadPolicy2: 1,
        playlist: this.videoId,
      };
    },
  }
}
</script>

<style>
.box {
  /* % 로 줘야 grid가 먹힌다. */
  width: 100%;
  height: 43rem;
}
.size-mini {
  width: 300px;
  height: 300px;
}
.size-default {
  width: 100%;
  height:100%;
}
</style>