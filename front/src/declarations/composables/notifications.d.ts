export namespace Notifications {
  export type NotificationParamsType = {
    message?: string;
    color?: string;
    type?: string;
    position?:
      | 'top-left'
      | 'top-right'
      | 'bottom-left'
      | 'bottom-right'
      | 'top'
      | 'bottom'
      | 'left'
      | 'right'
      | 'center';
    textColor?: string;
    timeout?: number;
    actions?: any[];
  };

  export type NotificationTypes = {
    error: (message?: string) => void;
    warning: (message?: string) => void;
    success: (message?: string) => void;
    info: (message?: string) => void;
  };
}
