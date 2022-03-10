<template>
  <div class="star">
    <div class="star-ratings">
      <div
        class="star-ratings-fill space-x-2 text-lg"
        :style="{ width: `${starPercentage}` + '%' }"
      >
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
      </div>
      <div class="star-ratings-base space-x-2 text-lg">
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
        <font-awesome-icon :icon="['fas', 'star']" size="lg"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Star',
  props: {
    score: {
      type: Number
    },
  },
  computed: {
    starPercentage() {
      return (this.score / 10) * 100
    }
  }
}
</script>
<style scoped>
.star-ratings {
  position: relative;
  width: max-content;
  -webkit-text-fill-color: transparent; /* Will override color (regardless of order) */
  -webkit-text-stroke-width: 1.3px;
  -webkit-text-stroke-color: #2b2a29;
}

.star-ratings-fill {
  color: gold;
  padding: 0;
  position: absolute;
  display: flex;
  top: 0;
  left: 0;
  overflow: hidden;
  -webkit-text-fill-color: gold;
}

.star-ratings-base {
  z-index: 0px;
  padding: 0px;
  color: rgb(15, 12, 29);
}

</style>
