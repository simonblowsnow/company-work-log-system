<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/*每个页面公共css */
	.uni-radio-input{ width: 16px!important; height: 16px!important;  }
	/* .uni-slider-thumb{ width: 20px!important; height: 20px!important;    margin-left: -10px!important; margin-top: -10px!important;  } */
	.uni-collapse-cell--open { background-color: #fff!important }
	.uni-popup__wrapper-box {
		width: 85%!important; 
	}
	.uni-combox__input .uni-input-input { 
		font-size: 28rpx!important; 
		color: #666;
	}
	.progress .uni-slider {
		margin-left: 12px!important;
	}
	.progress .uni-slider-thumb {
		width: 20px!important;
		height: 20px!important;
		margin-top: -10px!important;
		margin-left: -10px!important;
	}

    /*.uni-field-inner {*/
    /*    -webkit-box-align: start!important;*/
    /*    -webkit-align-items: flex-start!important;*/
    /*    align-items: start!important;*/
    /*}*/
    /*.createPopLine { flex-direction: inherit!important; }*/

</style>
