package br.com.intelie.google_search_util;

import java.util.ArrayList;
import java.util.List;

import org.junit.Assert;
import org.junit.Test;

import br.com.intelie.google_search_util.util.Util;

public class TestUtil {

	@Test
	public void testOccurrencesCount(){
		
		Util utilTest = new Util();
		
		List<String> listTest = new ArrayList<String>();
		listTest.add("Essa é uma string de teste que contém livro, lirvo e lriov");
		listTest.add("Essa string não contém a palava");
		
		Assert.assertEquals(Integer.valueOf(2), utilTest.occurrencesCount(listTest, "livro"));
		
	}
}
