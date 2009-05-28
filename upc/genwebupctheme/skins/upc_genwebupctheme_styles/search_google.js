/* Script per seleccionar el cercador de Plone o el de Google (GSA)*/

	function mostram(){
		
		checkbox = jq('#CheckCercaLSBox').attr('checked');
		if (checkbox)
		{
			jq('#LSResult').show();
		    url=jq('#plone_search_url').attr('value');
		    jq('#livesearch0').attr('action',url);
		    jq('#searchGadget').show();
		    jq('#q').hide();
		    jq('#searchGadget').attr('style', 'background-color:#F1F8E5');
		}
		else
		{ 
			jq('#LSResult').hide();		
			jq('#plone_search_url').hide();
		    jq('#livesearch0').attr('action','http://cercador.upc.edu/cercaUPC/search');
		    jq('#searchGadget').hide();
		    jq('#q').show();		    
		}
	}

/* END */