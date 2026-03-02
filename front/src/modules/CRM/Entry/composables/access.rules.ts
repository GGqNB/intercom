import {required, minLength, email, alpha  } from '@vuelidate/validators';

// const russianLettersRegex = /^[а-яА-ЯёЁ]+$/;
export const CREATE_SERVICE = {
  name: {
    required,
    minLength: minLength(4),
  },
  fullname: {
    required,
    minLength: minLength(4),
  },
  sp_process_template_id: {
    required,
  },
  code: {
    required,
    minLength: minLength(4),
  },
  mnemonic: {
    required,
    minLength: minLength(4),
  },
};
  
