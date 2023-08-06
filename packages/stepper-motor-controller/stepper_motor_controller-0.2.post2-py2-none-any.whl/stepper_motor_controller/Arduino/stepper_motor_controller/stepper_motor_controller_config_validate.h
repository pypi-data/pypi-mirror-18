#ifndef ___STEPPER_MOTOR_CONTROLLER_CONFIG_VALIDATE___
#define ___STEPPER_MOTOR_CONTROLLER_CONFIG_VALIDATE___

namespace stepper_motor_controller {
namespace config_validate {

template <typename NodeT>
struct OnConfigI2cAddressChanged : public ScalarFieldValidator<uint32_t, 1> {
  typedef ScalarFieldValidator<uint32_t, 1> base_type;

  NodeT *node_p_;
  OnConfigI2cAddressChanged() : node_p_(NULL) {
    this->tags_[0] = 3;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(uint32_t &source, uint32_t target) {
    if (node_p_ != NULL) { return node_p_->on_config_i2c_address_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnConfigMicrostepSettingChanged : public ScalarFieldValidator<uint32_t, 1> {
  typedef ScalarFieldValidator<uint32_t, 1> base_type;

  NodeT *node_p_;
  OnConfigMicrostepSettingChanged() : node_p_(NULL) {
    this->tags_[0] = 51;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(uint32_t &source, uint32_t target) {
    if (node_p_ != NULL) { return node_p_->on_config_microstep_setting_changed(source); }
    return false;
  }
};

template <typename NodeT>
class Validator : public MessageValidator<2> {
public:
  OnConfigI2cAddressChanged<NodeT> i2c_address_;
  OnConfigMicrostepSettingChanged<NodeT> microstep_setting_;

  Validator() {
    register_validator(i2c_address_);
    register_validator(microstep_setting_);
  }

  void set_node(NodeT &node) {
    i2c_address_.set_node(node);
    microstep_setting_.set_node(node);
  }
};

}  // namespace config_validate
}  // namespace stepper_motor_controller

#endif  // #ifndef ___STEPPER_MOTOR_CONTROLLER_CONFIG_VALIDATE___
    
