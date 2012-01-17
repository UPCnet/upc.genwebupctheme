/* Script per seleccionar el cercador de Plone o el de Google (GSA)*/

	function mostram(){
		
		checkbox = jq('#CheckCercaLSBox').attr('checked');
		if (checkbox)
		{
			jq('#LSResult').show();
		    url=jq('#plone_search_url').attr('value');
		    jq('#livesearch0').attr('action',url);
            //Cridem a la funcio customotizada de livesearch.js
		    livesearch.set_target("0",url)
		    jq('#q').hide();
		    jq('#searchGadget').attr('style', 'background-color:#F1F8E5');
		}
		else
		{ 
			jq('#LSResult').hide();		
			jq('#plone_search_url').hide();            
		    jq('#livesearch0').attr('action','http://cercador.upc.edu/cercaUPC/search');
            //Cridem a la funcio customotizada de livesearch.js
            livesearch.set_target("0",url)
		    jq('#searchGadget').hide();
		    jq('#q').show();		    
		}
	}

/* END */