/* 검색버튼 눌렀을 때 팝업 */

function fn_myFn() {
	let timerInterval
Swal.fire({
title: '목줄챙겨 주인!!',
html: '공원까지 <b></b> 걸음 남음...',
timer: 2000,
backdrop: `
rgba(255, 255, 255, .45)
url("/data/dog.png")
27% 25%
no-repeat
`,

timerProgressBar: true,
didOpen: () => {
	Swal.showLoading()
	
	const b = Swal.getHtmlContainer().querySelector('b')
	timerInterval = setInterval(() => {
		b.textContent = Swal.getTimerLeft()}, 100)},
	
willClose: () => {
	clearInterval(timerInterval)}}).then((result) => {
		if (result.dismiss === Swal.DismissReason.timer) {
			Swal.fire("나가쟈!!")}
		})
		
		window.myForm.submit();
	}