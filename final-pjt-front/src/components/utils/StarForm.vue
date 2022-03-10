<template>
  <div>
    <div class="rating-container">
      <div class="rating-wrap">
        <div class="center">
          <fieldset class="rating">
            <input type="radio" :id="`${isUpdating}star10`" name="rating" value="10" @input="updateRating" :checked="this.initialRank == 10"/><label :for="`${isUpdating}star10`" class="full" title="Awesome"></label>
            <input type="radio" :id="`${isUpdating}star9`" name="rating" value="9" @input="updateRating" :checked="this.initialRank == 9"/><label :for="`${isUpdating}star9`" class="half"></label>
            <input type="radio" :id="`${isUpdating}star8`" name="rating" value="8" @input="updateRating" :checked="this.initialRank == 8"/><label :for="`${isUpdating}star8`" class="full"></label>
            <input type="radio" :id="`${isUpdating}star7`" name="rating" value="7" @input="updateRating" :checked="this.initialRank == 7"/><label :for="`${isUpdating}star7`" class="half"></label>
            <input type="radio" :id="`${isUpdating}star6`" name="rating" value="6" @input="updateRating" :checked="this.initialRank == 6"/><label :for="`${isUpdating}star6`" class="full"></label>
            <input type="radio" :id="`${isUpdating}star5`" name="rating" value="5" @input="updateRating" :checked="this.initialRank == 5"/><label :for="`${isUpdating}star5`" class="half"></label>
            <input type="radio" :id="`${isUpdating}star4`" name="rating" value="4" @input="updateRating" :checked="this.initialRank == 4"/><label :for="`${isUpdating}star4`" class="full"></label>
            <input type="radio" :id="`${isUpdating}star3`" name="rating" value="3" @input="updateRating" :checked="this.initialRank == 3"/><label :for="`${isUpdating}star3`" class="half"></label>
            <input type="radio" :id="`${isUpdating}star2`" name="rating" value="2" @input="updateRating" :checked="this.initialRank == 2"/><label :for="`${isUpdating}star2`" class="full"></label>
            <input type="radio" :id="`${isUpdating}star1`" name="rating" value="1" @input="updateRating" :checked="this.initialRank == 1"/><label :for="`${isUpdating}star1`" class="half"></label>
          </fieldset>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Test',
  props: {
    initialRank: {
      type: String
    }
  },
  methods:{
    updateRating(event) {
      if (this.isUpdating) {
        this.$emit('target-rating-input', event.target.value)
      } else {
        this.$emit('rating-input', event.target.value)
      }
    }
  },
  computed: {
    isUpdating() {
      return this.initialRank === '0' ? '' : 'updating-'
    }
  }
}
</script>

<style scoped>
@import url(https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css);


.rating-wrap{
	max-width: 480px;
	/* margin: auto; */
	box-shadow: 0 0 3px 0 rgba(0,0,0,.2);
}

/*styling star rating*/
.rating{
	border: none;
	float: right;
}

.rating > input{
	display: none;
}

.rating > label:before{
  /* f0eb */
	content: '\f005';
	font-family: FontAwesome;
	margin-right: 2px;
	font-size: 1.6rem;
	display: inline-block;
	cursor: pointer;
}

.rating > .half:before{
	content: '\f089';
	position: absolute;
	cursor: pointer;
}

.rating > label{
	color: #ddd;
	float: right;
	cursor: pointer;
}

.rating > input:checked ~ label,
.rating:not(:checked) > label:hover, 
.rating:not(:checked) > label:hover ~ label{
	color: rgb(155, 93, 255);
}

.rating > input:checked + label:hover,
.rating > input:checked ~ label:hover,
.rating > label:hover ~ input:checked ~ label,
.rating > input:checked ~ label:hover ~ label{
	color: rgb(155, 93, 255);
}

</style>