var profileOn = document.querySelector('#profileOn');
var closeProfile = document.querySelector('#closeProfile')
var profileBox = document.querySelector('#userProfile');

profileOn.addEventListener('click', function() {
	profileBox.style.display="block";
 });

closeProfile.addEventListener('click', function() {
profileBox.style.display="none";
});