<template>
  <div>
    <b-sidebar
      id="sidebar-border"
      sidebar-class="border-color"
      header-class="sidebar-color"
      body-class="sidebar-color"
      class="title-margin"
      width="30em"
      shadow="lg"
      :backdrop-variant="variant"
      backdrop
    >
      <h3 class="side-title">MOVIE OST</h3>
      <div class="px-3 py-2">
        <search-form :from="'sidebar'"></search-form>
        <p>
          영화의 OST를 검색해 보세요.
        </p>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
import SearchForm from '@/components/utils/SearchForm'

export default {
  name: 'Sidebar',
  data() {
    return {
      variant: 'dark',
    }
  },
  components: {
    SearchForm
  }
}
</script>

<style scoped>
.side-title {
  text-align: left;
  margin-left: 2.5rem;
  font-weight: bold;
}
.sidebar-color {
  background-color: rgb(255, 212, 82);
}
.border-color {
  border-right: 2px solid rgb(248, 63, 94);
}
</style>