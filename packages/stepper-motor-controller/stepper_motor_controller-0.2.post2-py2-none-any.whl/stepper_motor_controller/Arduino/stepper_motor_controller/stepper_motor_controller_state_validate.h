#ifndef ___STEPPER_MOTOR_CONTROLLER_STATE_VALIDATE___
#define ___STEPPER_MOTOR_CONTROLLER_STATE_VALIDATE___

namespace stepper_motor_controller {
namespace state_validate {

template <typename NodeT>
class Validator : public MessageValidator<0> {
public:

  Validator() {
  }

  void set_node(NodeT &node) {
  }
};

}  // namespace state_validate
}  // namespace stepper_motor_controller

#endif  // #ifndef ___STEPPER_MOTOR_CONTROLLER_STATE_VALIDATE___
    
