/**
 * Agent
 */
class Agent {
  parser = null;
  os = null;
  browser = null;
  bluetooth = null;

  constructor() {
    this.parser = new UAParser();
    this.initialize();
  }

  initialize() {
    const agent = this.parser.getResult();
    this.set("os", `${agent.os.name} (${agent.os.version})`);
    this.set("browser", `${agent.browser.name} (${agent.browser.version})`);
  }

  set(id, text) {
    this[id] = text;
    document.getElementById(id).innerText = text ?? "Unknown";
  }
}

/**
 * Bluetooth
 */
class Bluetooth {
  error = null;
  status = null;
  supported = false;

  constructor() {
    this.setup();
  }

  async setup() {
    await this.checkStatus();
    this.setAgent();
  }

  setAgent() {
    switch (true) {
      // not supported, return early
      case !this.supported:
        return Austramax.agent.set("bluetooth", "Not supported");

      // error while checking status
      case Boolean(this.error):
        return Austramax.agent.set("bluetooth", "Error checking status");

      // supported, but previously denied
      case this.status.state === "denied":
        return Austramax.agent.set("bluetooth", "Denied (retry)");

      // supported, but previously denied
      case this.status.state === "prompt":
        Austramax.agent.set("bluetooth", "Enable");
        return;

      // supported, but previously denied
      case this.status.state === "granted":
        Austramax.agent.set("bluetooth", "Enabled");
        return;

      // unknown outcome
      default:
        return Austramax.agent.set("bluetooth", "Unknown");
    }
  }

  async checkStatus() {
    Austramax.agent.set("bluetooth", "Checking...");
    this.supported = await navigator.bluetooth.getAvailability();

    // return early if not supported by device
    if (!this.supported) {
      return;
    }

    // check permission status
    try {
      this.status = await navigator.permissions.query({ name: "bluetooth" });
      this.status.onchange = this.onStatusChange;
    } catch (error) {
      this.error = error;
      return;
    }
  }

  onStatusChange(event) {
    console.log("Bluetooth.status.chanaged", event);
    this.setAgent();
  }
}

/**
 *
 */
class Network {
  connection = null;

  constructor() {
    this.connection = navigator.connection ?? null;
    if (this.connection) {
      this.connection.onchange = this.onChange;
    }

    this.setAgent();
  }

  setAgent() {
    switch (true) {
      // not connected
      case !this.connection:
        return Austramax.agent.set("network", "Offline");

      // connected to the internet
      default:
        return Austramax.agent.set("network", "Online");
    }
  }

  onChange(event) {
    console.log("Network.connection.chanaged", event);
    this.setAgent();
  }
}

/**
 * Austramax
 */
const Austramax = {};
Austramax.agent = new Agent();
Austramax.bluetooth = new Bluetooth();
Austramax.network = new Network();
window.austramax = Austramax;
console.log(Austramax);
