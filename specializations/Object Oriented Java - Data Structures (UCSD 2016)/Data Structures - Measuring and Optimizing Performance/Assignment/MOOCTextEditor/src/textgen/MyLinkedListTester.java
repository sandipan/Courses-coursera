/**
 * 
 */
package textgen;

import static org.junit.Assert.*;

import java.util.LinkedList;

import org.junit.Before;
import org.junit.Test;

/**
 * @author UC San Diego MOOC team
 *
 */
public class MyLinkedListTester {

	private static final int LONG_LIST_LENGTH =10; 

	MyLinkedList<String> shortList;
	MyLinkedList<Integer> emptyList;
	MyLinkedList<Integer> longerList;
	MyLinkedList<Integer> list1;
	
	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception {
		// Feel free to use these lists, or add your own
	    shortList = new MyLinkedList<String>();
		shortList.add("A");
		shortList.add("B");
		emptyList = new MyLinkedList<Integer>();
		longerList = new MyLinkedList<Integer>();
		for (int i = 0; i < LONG_LIST_LENGTH; i++)
		{
			longerList.add(i);
		}
		list1 = new MyLinkedList<Integer>();
		list1.add(65);
		list1.add(21);
		list1.add(42);
		
	}

	
	/** Test if the get method is working correctly.
	 */
	/*You should not need to add much to this method.
	 * We provide it as an example of a thorough test. */
	@Test
	public void testGet()
	{
		//test empty list, get should throw an exception
		try {
			emptyList.get(0);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		
		// test short list, first contents, then out of bounds
		assertEquals("Check first", "A", shortList.get(0));
		assertEquals("Check second", "B", shortList.get(1));
		
		try {
			shortList.get(-1);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		try {
			shortList.get(2);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		// test longer list contents
		for(int i = 0; i<LONG_LIST_LENGTH; i++ ) {
			assertEquals("Check "+i+ " element", (Integer)i, longerList.get(i));
		}
		
		// test off the end of the longer array
		try {
			longerList.get(-1);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		try {
			longerList.get(LONG_LIST_LENGTH);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		}
		
	}
	
	
	/** Test removing an element from the list.
	 * We've included the example from the concept challenge.
	 * You will want to add more tests.  */
	@Test
	public void testRemove()
	{
		int a = list1.remove(0);
		assertEquals("Remove: check a is correct ", 65, a);
		assertEquals("Remove: check element 0 is correct ", (Integer)21, list1.get(0));
		assertEquals("Remove: check size is correct ", 2, list1.size());
		try {
			list1.remove(2);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		a = list1.remove(1);
		assertEquals("Remove: check a is correct ", 42, a);
		assertEquals("Remove: check element 0 is correct ", (Integer)21, list1.get(0));
		assertEquals("Remove: check size is correct ", 1, list1.size());
		a = list1.remove(0);
		assertEquals("Remove: check a is correct ", 21, a);
		assertEquals("Remove: check size is correct ", 0, list1.size());
		try {
			list1.remove(0);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		
		// TODO: Add more tests here
		//test empty list, get should throw an exception
		try {
			emptyList.remove(0);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
				
		// test short list, first contents, then out of bounds
		try {
			shortList.remove(2);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		assertEquals("Check first", "A", shortList.remove(0));
		assertEquals("Check second", "B", shortList.remove(0));
		
		try {
			shortList.remove(-1);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		
		// test longer list contents
		for(int i = LONG_LIST_LENGTH - 1; i >= 0; --i) {
			assertEquals("Check "+i+ " element", (Integer)i, longerList.remove(i));
			assertEquals("Check size", i, longerList.size());
		}
				
		// test off the end of the longer array
		try {
			longerList.remove(-1);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		
		}
		try {
			longerList.remove(LONG_LIST_LENGTH);
			fail("Check out of bounds");
		}
		catch (IndexOutOfBoundsException e) {
		}
	}
	
	/** Test adding an element into the end of the list, specifically
	 *  public boolean add(E element)
	 * */
	@Test
	public void testAddEnd()
	{
        // TODO: implement this test
		list1.add(12);
		assertEquals("Remove: check add is correct ", (Integer)12, list1.get(3));
		assertEquals("Remove: check element 2 is correct ", (Integer)42, list1.get(2));
		assertEquals("Remove: check size is correct ", 4, list1.size());
		try {
			list1.add(null);
			fail("Check null element");
		}
		catch (NullPointerException e) {
			
		}
		
		// TODO: Add more tests here
		//test empty list, get should throw an exception
		emptyList.add(1);
		assertEquals("Remove: check add is correct ", (Integer)1, emptyList.get(0));
		assertEquals("Remove: check size is correct ", 1, emptyList.size());
		
		// test short list, first contents, then out of bounds
		try {
			shortList.add(null);
			fail("Check null element");
		}
		catch (NullPointerException e) {
		
		}
		shortList.add("B");
		assertEquals("Remove: check size is correct ", 3, shortList.size());
		shortList.add("C");
		assertEquals("Remove: check size is correct ", 4, shortList.size());
		assertEquals("Check first", "A", shortList.get(0));
		assertEquals("Check second", "B", shortList.get(1));
		assertEquals("Check third", "B", shortList.get(2));
		assertEquals("Check fourth", "C", shortList.get(3));
		
		
		// test longer list contents
		for(int i = 0; i < LONG_LIST_LENGTH; ++i) {
			longerList.remove(0);
			longerList.add(i);
			assertEquals("Check size", LONG_LIST_LENGTH, longerList.size());
		}
		assertEquals("Check size", LONG_LIST_LENGTH, longerList.size());
		for(int i = 0; i<LONG_LIST_LENGTH; i++ ) {
			assertEquals("Check "+i+ " element", (Integer)i, longerList.get(i));
		}		
		// test off the end of the longer array
		try {
			longerList.add(null);
			fail("Check null element");
		}
		catch (NullPointerException e) {
		
		}		
	}

	
	/** Test the size of the list */
	@Test
	public void testSize()
	{
		// TODO: implement this test
		list1.add(12);
		assertEquals("Remove: check size is correct ", 4, list1.size());
		list1.remove(0);
		assertEquals("Remove: check size is correct ", 3, list1.size());
		list1.get(0);
		assertEquals("Remove: check size is correct ", 3, list1.size());
		try {
			list1.add(null);
			fail("Check null element");
		}
		catch (NullPointerException e) {
			
		}
		assertEquals("Remove: check size is correct ", 3, list1.size());
		list1.add(3, 12);
		assertEquals("Remove: check size is correct ", 4, list1.size());
		try {
			list1.add(5, 12);
			fail("Check out of bound");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		assertEquals("Remove: check size is correct ", 4, list1.size());
		
	}

	
	
	/** Test adding an element into the list at a specified index,
	 * specifically:
	 * public void add(int index, E element)
	 * */
	@Test
	public void testAddAtIndex()
	{
        // TODO: implement this test
		list1.add(0, 12);
		assertEquals("Remove: check add is correct ", (Integer)12, list1.get(0));
		assertEquals("Remove: check element 1 is correct ", (Integer)65, list1.get(1));
		assertEquals("Remove: check size is correct ", 4, list1.size());
		try {
			list1.add(0, null);
			fail("Check null element");
		}
		catch (NullPointerException e) {
			
		}
		assertEquals("Remove: check size is correct ", 4, list1.size());
		try {
			list1.add(5, 1);
			fail("Check index out of bound");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		assertEquals("Remove: check size is correct ", 4, list1.size());
		try {
			list1.add(-5, 1);
			fail("Check index out of bound");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		assertEquals("Remove: check size is correct ", 4, list1.size());
		list1.add(4, 1);
		assertEquals("Remove: check element 4 is correct ", (Integer)1, list1.get(4));
		assertEquals("Remove: check element 3 is correct ", (Integer)42, list1.get(3));
		assertEquals("Remove: check size is correct ", 5, list1.size());
		
		list1.add(2, 11);
		assertEquals("Remove: check element 2 is correct ", (Integer)11, list1.get(2));
		assertEquals("Remove: check element 3 is correct ", (Integer)21, list1.get(3));
		assertEquals("Remove: check element 1 is correct ", (Integer)65, list1.get(1));
		assertEquals("Remove: check size is correct ", 6, list1.size());
			
		
	}
	
	/** Test setting an element in the list */
	@Test
	public void testSet()
	{
	    // TODO: implement this test
		list1.set(0, 12);
		assertEquals("Remove: check add is correct ", (Integer)12, list1.get(0));
		assertEquals("Remove: check element 1 is correct ", (Integer)21, list1.get(1));
		assertEquals("Remove: check size is correct ", 3, list1.size());
		try {
			list1.set(0, null);
			fail("Check null element");
		}
		catch (NullPointerException e) {
			
		}
		assertEquals("Remove: check size is correct ", 3, list1.size());
		try {
			list1.set(5, 1);
			fail("Check index out of bound");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		assertEquals("Remove: check size is correct ", 3, list1.size());
		try {
			list1.set(-5, 1);
			fail("Check index out of bound");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
		assertEquals("Remove: check size is correct ", 3, list1.size());
		list1.set(2, 1);
		assertEquals("Remove: check element 2 is correct ", (Integer)1, list1.get(2));
		assertEquals("Remove: check element 1 is correct ", (Integer)21, list1.get(1));
		assertEquals("Remove: check size is correct ", 3, list1.size());
		
		list1.set(1, 11);
		assertEquals("Remove: check element 1 is correct ", (Integer)11, list1.get(1));
		assertEquals("Remove: check element 2 is correct ", (Integer)1, list1.get(2));
		assertEquals("Remove: check element 0 is correct ", (Integer)12, list1.get(0));
		assertEquals("Remove: check size is correct ", 3, list1.size());
		
		try {
			emptyList.set(0,1);
			fail("Check null element");
		}
		catch (IndexOutOfBoundsException e) {
			
		}
	}
	
	
	// TODO: Optionally add more test methods.
	
}
