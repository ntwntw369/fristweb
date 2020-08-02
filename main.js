function go(){
	var input;
	input = prompt('소원을 말해봐', '내 소원은..');
	document.write("<h1>너의 소원 '"+input+"'은 잘 받았다.</h>");
	setTimeout(function() {
	location.href=location.href;
	}, 3000);

}

	
const myHeading = document.querySelector('h2');
myHeading.textContent = 'Hi, World!';







