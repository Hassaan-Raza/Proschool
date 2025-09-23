```javascript
// Import necessary libraries
import $ from 'jquery';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles.css';

// Define a function to handle form submission
function handleSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());
  console.log(data);
}

// Define a function to handle button click
function handleClick() {
  console.log('Button clicked!');
}

// Define a function to handle dropdown change
function handleDropdownChange(event) {
  console.log(event.target.value);
}

// Add event listeners to elements
$('#myForm').on('submit', handleSubmit);
$('#myButton').on('click', handleClick);
$('#myDropdown').on('change', handleDropdownChange);

// Initialize the application
$(document).ready(function() {
  console.log('Application initialized!');
});
```