var hamBurger = document.querySelector('#ham-burger');
var closeBtn = document.querySelector('#close-btn');
var mobileLiTwo = document.querySelector('#mobile-li-two');
var mobileLiThree = document.querySelector('#mobile-li-three');
var signUpBox = document.querySelector('#signup-box');
var loginBox = document.querySelector('#login-box');
var adminBtn1 = document.querySelector('.admin-panel1');
var adminBtn2 = document.querySelector('.admin-panel2');
var adminPanel = document.querySelector('.admin-panel-form');
var closeAdmin = document.querySelector('#closeAdmin');




adminBtn1.addEventListener('click', function(){
   loginBox.style.opacity='0.2';
   signUpBox.style.opacity='0.2';
   adminPanel.style.display='block';
});
adminBtn2.addEventListener('click', function(){
   loginBox.style.opacity='0.2';
   signUpBox.style.opacity='0.2';
   document.querySelector('#mobile-nav').style.display='none';
   adminPanel.style.display='block';
});

closeAdmin.addEventListener('click', function(){
   loginBox.style.opacity='1';
   signUpBox.style.opacity='1';
   adminPanel.style.display='none';
});

function goToSignUp(){
   loginBox.style.transition='1s ease-in-out';
   loginBox.style.transform= "rotateY(360deg)";
            
   setTimeout( () => { 
      loginBox.style.display='none';
      document.querySelector('#signup-box').style.display='flex'; 
      loginBox.style.transform= "rotateY(0deg)";
      }, 500);
}
function goToLogIn(){         
   signUpBox.style.transition='1s ease-in-out';
   signUpBox.style.transform = "rotateY(360deg)";         
   setTimeout( () => { 
      signUpBox.style.display='none';
      document.querySelector('#login-box').style.display='flex'; 
      signUpBox.style.transform = "rotateY(0deg)";
      }, 500);
}
hamBurger.addEventListener('click',function(){
   mobileNav = document.querySelector('#mobile-nav').style.display='flex';
   
});
closeBtn.addEventListener('click',function(){
   document.querySelector('#mobile-nav').style.display='none';
   
});
mobileLiTwo.addEventListener('click',function(){
   document.location.href = '#about-section';
   document.querySelector('#mobile-nav').style.display='none';
   return false;
});
mobileLiThree.addEventListener('click',function(){
   document.location.href = '#contact-section';
   document.querySelector('#mobile-nav').style.display='none';
   return false;
});

