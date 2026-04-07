declare module 'usb' {
  export class Device {
    deviceDescriptor: {
      idVendor: number;
      idProduct: number;
    };
    allConfigDescriptors: ConfigDescriptor[];
    open(): void;
    close(): void;
    setAutoDetachKernelDriver(autoDetach: boolean): void;
    interface(interfaceNumber: number): Interface;
    reset(): void;
  }

  export class Interface {
    device: Device;
    interfaceNumber: number;
    claim(): void;
    release(): void;
    endpoint(address: number): Endpoint;
    isKernelDriverActive(): boolean;
    detachKernelDriver(): void;
    attachKernelDriver(): void;
  }

  export class Endpoint {
    address: number;
    direction: 'in' | 'out';
    transferType: number;
    descriptor: EndpointDescriptor;
    transfer(buffer: Buffer, callback?: (error: any) => void): void;
    transferAsync(buffer: Buffer): Promise<void>;
  }

  export interface EndpointDescriptor {
    bEndpointAddress: number;
    bmAttributes: number;
    wMaxPacketSize: number;
  }

  export interface ConfigDescriptor {
    interfaces: InterfaceDescriptor[][];
  }

  export interface InterfaceDescriptor {
    bInterfaceNumber: number;
    bAlternateSetting: number;
    bNumEndpoints: number;
  }

  export function findByIds(vendorId: number, productId: number): Device | undefined;
}
