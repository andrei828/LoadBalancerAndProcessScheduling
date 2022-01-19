import { AbstractControl, FormGroup, ValidationErrors, ValidatorFn } from "@angular/forms";

export interface ArrayLenghtValidatorOptions {
  min?: number;
  max?: number;
}

export function ArrayLenghtValidator(options: ArrayLenghtValidatorOptions): ValidatorFn {
  const fn: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const array = control.value as any[];
    const errors: any = {};
    const length = array.length;
    if(options.min != null && length < options.min) {
      errors["lessThan"] = options.min;
    }
    if(options.max != null && length > options.max) {
      errors["greatherThan"] = options.max;
    }
    return Object.keys(errors).length > 0 ? errors : null;
  }
  return fn;
}