

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
function postdata(result)
{
	
	$.ajax({
		type: "POST",
		url: "order_fin/",
		data: { csrfmiddlewaretoken: document.getElementById("csr").className , 'pro_name': result},  
		success: function (data) {
			document.getElementById("it").innerHTML = "Robot coming"
			location.reload();
			
		}
	});
	
	//location.reload();
}


function calculat( cartsck) {
	
	var id = "id" + cartsck.slice(2);
var name = document.getElementById(id).innerHTML;

postdata(name);
	
};


dev.forEach(function(link){

	link.addEventListener("click", function () {
		var dv = link.getAttribute("id");
		  
		if (dv != null) {
			var quantiy = " ";
			  
			ina.forEach(function (link) {
				  
				
			  
				pa.forEach(function (link) {
				  
					var paa = link.getAttribute("id");
					if (paa != null) {
						if (paa.slice(2) == dv.slice(2)) {
	
					
							calculat(paa);
						}
					}
				});
			  
		
		
			});
		}
	});
	
	
	});



// document.getElementById("Order_pro").addEventListener("click", function() {
	
// 	$.ajax({
// 		type: "GET",
// 		url: 'order_res/',
// 		data: { csrfmiddlewaretoken: '{{ csrf_token }}' , text: "text" },  
// 		success: function(data) {
			
// 			location.reload();
// 		}

// 	});
	
// });

