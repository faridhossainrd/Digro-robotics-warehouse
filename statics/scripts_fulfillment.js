

var dev = document.querySelectorAll("div");
var ina = document.querySelectorAll("input");
var pa = document.querySelectorAll("p");
var k = 0;


var quentitys= [];

function cancel_order() {
	
	quentitys= [];

	document.getElementById("it").innerHTML = "0";
	document.getElementById("am").innerHTML ="৳ "+  "0";
}


function calculat( Qnck ,price,quantiy ) {

				// console.log(Qnck)
				// console.log(quantiy)
				// console.log(quantiy)
				var qck = true;
				if (quentitys[0] == NaN)
				{
					var id = Qnck; 
					var quantiys =quantiy;
					var prices = price;
					
					quentitys.push({
						key:   id,
						value: [prices,quantiys] 
					});
			
				}
	
				for (const [key, value] of quentitys.entries()) {

			
					if (quentitys[key]["key"] == Qnck)
					{
						quentitys[key]["value"][1] = quantiy;
						quentitys[key]["value"][0] = price;
						qck = false;
					};
	            };
	
	if (qck)
	{
		var id = Qnck; 
		var quantiys =quantiy;
		var prices = price;
		
		quentitys.push({
			key:   id,
			value: [prices,quantiys] 
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

dev.forEach(function (link) {

	link.addEventListener("click", function () {

		var dv = link.getAttribute("id");

		if (dv != null) {

			 
			var Qnck = " ";
			var cart = " ";
			var quantiy = " ";


			ina.forEach(function (links) {
				
				var inv = links.getAttribute("id");
				
				if (inv != null) {
			           
					if(inv.slice(2) == dv.slice(2))
					{
						Qnck = inv.slice(3);
						quantiy = document.getElementById(inv).value;
						quantiy = parseInt(quantiy);
						Qnck = parseInt(Qnck);
						

					}

					
				}
				  
			});
			
			pa.forEach(function(link)
			{
				
			  var pa = link.getAttribute("id");
			  if(pa!=null)
			   {
				  if(pa.slice(2) == dv.slice(3))
				  {
					   
					  cart = document.getElementById(pa).innerHTML;
					  cart = cart.slice(1,(cart.length - 2));
					  cart = parseInt(cart);
					  
				  }
			}
			});

			if(quantiy!=" " && cart!=" ")
			{
				var price = cart * quantiy
                calculat(Qnck,price,quantiy);
			}

		}
		
		
		 
	});
});

document.getElementById("Cancel").addEventListener("click", function() {
	
	cancel_order();
	
});


function postdata(result)
{
	
	$.ajax({
		type: "POST",
		url: "",
		data: { csrfmiddlewaretoken: document.getElementById("csr").className , result: result },  
		success: function(data) {
			console.log(data);
		}
	});

	location.reload();
}


document.getElementById("submitid").addEventListener("click", function() {
	
	var result = JSON.stringify(quentitys);
	//var result = JSON.parse(result);
	//console.log(result);
	postdata(result)
	cancel_order();
});


