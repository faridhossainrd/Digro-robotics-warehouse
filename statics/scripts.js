

var dev = document.querySelectorAll("div");
var ina = document.querySelectorAll("input");
var pa = document.querySelectorAll("p");
var k = 0;


var quentitys= [];

function cancel_order() {
	
	quentitys= [];
	// for (const [key, value] of quentitys.entries()) {
		
	// 	delete quentitys[key];

	// };

	document.getElementById("it").innerHTML = "0";
	document.getElementById("am").innerHTML ="৳ "+  "0";
}

function calculat(carts, q,cartsck,Qnck) {
	
	var qck = true;

	if (quentitys[0] == NaN)
	{
		var id = "id" + cartsck.slice(2);
		var name = document.getElementById(id).innerHTML;
		
		quentitys.push({
			key:   name,
			value: [(carts * q), q] 
		});

		}

	for (const [key, value] of quentitys.entries()) {

		var id = "id" + cartsck.slice(2);
		var name = document.getElementById(id).innerHTML;

		if (quentitys[key]["key"] == name)
		{
			quentitys[key]["value"][0] = (carts * q);
			quentitys[key]["value"][1] = q;
			qck = false;
		};
	};

	if (qck)
	{
		var id = "id" + cartsck.slice(2);
		var name = document.getElementById(id).innerHTML;

		quentitys.push({
			key:   name,
			value: [(carts * q), q] 
		});

	};

	var totalq = 0;
	var totalc = 0;
	for (const [key, value] of quentitys.entries()) {
		
		
		totalc +=  parseInt(quentitys[key]["value"][0] );
		totalq += parseInt(quentitys[key]["value"][1] );

	};
	
	document.getElementById("it").innerHTML = totalq.toString();
	document.getElementById("am").innerHTML = "৳ " + totalc.toString();
	
	
	
};




dev.forEach(function(link){
	
	
	link.addEventListener("click", function(){
		  var dv = link.getAttribute("id");
		  
		  if(dv!=null)
		  {
			  var cartsck = " ";
			  var Qnck = " ";
			  var cart = " ";
			  var quantiy = " ";
			  
			  ina.forEach(function(link)
			  {
				  
				var inv = link.getAttribute("id");
				if(inv!=null)
		         {
				    if(inv.slice(2) == dv.slice(2))
					{
						Qnck = inv;
						//console.log(inv.slice(2));
						quantiy = document.getElementById(inv).value;
						quantiy = parseInt(quantiy);
					}
  
			  }
			  });
			  
			  pa.forEach(function(link)
			  {
				  
				var pa = link.getAttribute("id");
				if(pa!=null)
		         {
				    if(pa.slice(2) == dv.slice(2))
					{
						//console.log(pa.slice(2));
						cart =document.getElementById(pa).innerHTML;
						cart = cart.slice(1, (pa.length - 2));
						cart = parseInt(cart);
						cartsck = pa;
					}
			  }
			  });
			  
			 if(quantiy!=" " && cart!=" ")
			 {
				 //console.log(quantiy);
				 console.log(cart);
				 
				 // console.log(*parseInt(quantiy));
				 calculat(cart,quantiy,cartsck,Qnck);
			 }
		  }
		
		});
	
	
})

document.getElementById("Cancel").addEventListener("click", function() {
	
	cancel_order();
	
	
});


function postdata(result)
{
	
	$.ajax({
		type: "POST",
		url: 'orders/',
		data: { csrfmiddlewaretoken: document.getElementById("csr").className , result: result },  
		success: function(data) {
			console.log(data);
		}
	});


}


document.getElementById("submitid").addEventListener("click", function() {
	
	var result = JSON.stringify(quentitys);
	//var result = JSON.parse(result);
	//console.log(result);
	postdata(result)
	cancel_order();
});

/*
var msgArray = [0,0,0,0,0];

function myFunction() {
	var total = 0;
	for (i = 0; i < msgArray.length; i++) {
		total += parseInt(msgArray[i]);
  };
	
	document.getElementById("it").innerHTML = total;
};

document.getElementById("apple_action").addEventListener("click", function() {
	
	 msgArray[0]=document.getElementById("apple_quantity").value;
	 myFunction();
	 
	 
});

document.getElementById("Banana_action").addEventListener("click", function() {
	 
    msgArray[1]= document.getElementById("Banana_quantiy").value;

   myFunction();
});

document.getElementById("Grapes_action").addEventListener("click", function() {
	
  msgArray[2]= document.getElementById("Grapes_quantity").value;
    myFunction();
});

document.getElementById("Pineapple_action").addEventListener("click", function() {
	
  msgArray[3]=document.getElementById("Pineapple_quantity").value;
    myFunction();
});

document.getElementById("Strawberry_action").addEventListener("click", function() {

  msgArray[4]=document.getElementById("Strawberry_quantity").value;
    myFunction();
});


*/