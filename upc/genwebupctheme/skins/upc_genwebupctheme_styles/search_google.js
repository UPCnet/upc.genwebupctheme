/* Script per seleccionar el cercador de Plone o el de Google (GSA)*/

/* Aquest és el de Google*/
	function mostram(){
	    document.getElementById("LSBox").style.display="block";
	    document.getElementById("NoLSBox").style.display="none";
	    document.getElementById("CheckCercaLSBox").checked="";
	    document.getElementById("CheckCercaNoLSBox").checked="checked";
	}

	

/* I aquest el de Plone */
	function mostram2(){
	    document.getElementById("NoLSBox").style.display="block";
	    document.getElementById("LSBox").style.display="none";
	    document.getElementById("CheckCercaLSBox").checked="";
	    document.getElementById("CheckCercaNoLSBox").checked="checked";
	}


/* END */