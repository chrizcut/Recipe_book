function addIngredient() {
    const firstIngredient = document.querySelector('.ingredientField');
    if (!firstIngredient) return; // Safety check if no ingredient exists yet

    // const newIngredient = firstIngredient.cloneNode(true);
    const newIngredient = document.createElement('div');
    newIngredient.classList.add('ingredientField');
    newIngredient.innerHTML = firstIngredient.innerHTML;

    const newIndex = document.querySelectorAll('.ingredientField').length+1;

    // Update IDs and names
    const ingredient = newIngredient.querySelector('[id^="ingredients-"][id$="-ingredient"]');
    const quantity = newIngredient.querySelector('[id^="ingredients-"][id$="-quantity"]');

    if (ingredient) {
        ingredient.id = `ingredients-${newIndex}-ingredient`;
        ingredient.name = ingredient.id;
        ingredient.value = '';  // Clear value
    }

    if (quantity) {
        quantity.id = `ingredients-${newIndex}-quantity`;
        quantity.name = quantity.id;
        quantity.value = '';  // Clear value
    }

    document.getElementById('ingredientsContainer').appendChild(newIngredient);
    newIngredient.querySelector('input').focus(); // Focus on the new input
}

function removeIngredient() {
    const ingredientFields = document.querySelectorAll('.ingredientField');  // Get all the ingredient fields
    if (ingredientFields.length > 1) {  // Ensure there is more than one ingredient field to remove
        const lastIngredient = ingredientFields[ingredientFields.length - 1];  // Get the last ingredient field
        lastIngredient.remove();  // Remove the last ingredient field
    }
    return false;
}

function addStep() {
    const firstStep = document.querySelector('.stepField');
    if (!firstStep) return; // Safety check

    const newStep = firstStep.cloneNode(true);
    const newIndex = document.querySelectorAll('.stepField').length+1;

    // Update ID and name
    const body = newStep.querySelector('[id^="steps-"]');
    if (body) {
        body.id = `steps-${newIndex}-body`;
        body.name = body.id;
        body.value = ''; // Reset value
    }

    // Create an <h3> element for the step number
    const stepTitle = document.createElement('h3');
    stepTitle.textContent = `Step ${newIndex}`;

    // Insert step title before input field
    newStep.prepend(stepTitle);

    document.getElementById('stepsContainer').appendChild(newStep);
    newStep.querySelector('input').focus(); // Focus on new input
}

function removeStep() {
    const stepFields = document.querySelectorAll('.stepField'); // Get all step fields
    if (stepFields.length > 1) { // Ensure at least one remains
        const lastStep = stepFields[stepFields.length - 1]; // Get the last step field
        const lastStepTitle = lastStep.previousElementSibling; // Get the preceding <h3> title

        if (lastStepTitle && lastStepTitle.tagName === 'H3') {
            lastStepTitle.remove(); // Remove the title
        }

        lastStep.remove(); // Remove the step field
    }

    return false;
}