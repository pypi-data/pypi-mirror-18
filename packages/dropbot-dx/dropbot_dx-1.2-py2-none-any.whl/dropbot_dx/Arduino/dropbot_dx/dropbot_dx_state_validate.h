#ifndef ___DROPBOT_DX_STATE_VALIDATE___
#define ___DROPBOT_DX_STATE_VALIDATE___

namespace dropbot_dx {
namespace state_validate {

template <typename NodeT>
struct OnStateFrequencyChanged : public ScalarFieldValidator<float, 1> {
  typedef ScalarFieldValidator<float, 1> base_type;

  NodeT *node_p_;
  OnStateFrequencyChanged() : node_p_(NULL) {
    this->tags_[0] = 2;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(float &source, float target) {
    if (node_p_ != NULL) { return node_p_->on_state_frequency_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateHvOutputEnabledChanged : public ScalarFieldValidator<bool, 1> {
  typedef ScalarFieldValidator<bool, 1> base_type;

  NodeT *node_p_;
  OnStateHvOutputEnabledChanged() : node_p_(NULL) {
    this->tags_[0] = 3;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(bool &source, bool target) {
    if (node_p_ != NULL) { return node_p_->on_state_hv_output_enabled_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateHvOutputSelectedChanged : public ScalarFieldValidator<bool, 1> {
  typedef ScalarFieldValidator<bool, 1> base_type;

  NodeT *node_p_;
  OnStateHvOutputSelectedChanged() : node_p_(NULL) {
    this->tags_[0] = 4;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(bool &source, bool target) {
    if (node_p_ != NULL) { return node_p_->on_state_hv_output_selected_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateLightEnabledChanged : public ScalarFieldValidator<bool, 1> {
  typedef ScalarFieldValidator<bool, 1> base_type;

  NodeT *node_p_;
  OnStateLightEnabledChanged() : node_p_(NULL) {
    this->tags_[0] = 5;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(bool &source, bool target) {
    if (node_p_ != NULL) { return node_p_->on_state_light_enabled_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateMagnetEngagedChanged : public ScalarFieldValidator<bool, 1> {
  typedef ScalarFieldValidator<bool, 1> base_type;

  NodeT *node_p_;
  OnStateMagnetEngagedChanged() : node_p_(NULL) {
    this->tags_[0] = 6;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(bool &source, bool target) {
    if (node_p_ != NULL) { return node_p_->on_state_magnet_engaged_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateVoltageChanged : public ScalarFieldValidator<float, 1> {
  typedef ScalarFieldValidator<float, 1> base_type;

  NodeT *node_p_;
  OnStateVoltageChanged() : node_p_(NULL) {
    this->tags_[0] = 1;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(float &source, float target) {
    if (node_p_ != NULL) { return node_p_->on_state_voltage_changed(source); }
    return false;
  }
};

template <typename NodeT>
class Validator : public MessageValidator<6> {
public:
  OnStateFrequencyChanged<NodeT> frequency_;
  OnStateHvOutputEnabledChanged<NodeT> hv_output_enabled_;
  OnStateHvOutputSelectedChanged<NodeT> hv_output_selected_;
  OnStateLightEnabledChanged<NodeT> light_enabled_;
  OnStateMagnetEngagedChanged<NodeT> magnet_engaged_;
  OnStateVoltageChanged<NodeT> voltage_;

  Validator() {
    register_validator(frequency_);
    register_validator(hv_output_enabled_);
    register_validator(hv_output_selected_);
    register_validator(light_enabled_);
    register_validator(magnet_engaged_);
    register_validator(voltage_);
  }

  void set_node(NodeT &node) {
    frequency_.set_node(node);
    hv_output_enabled_.set_node(node);
    hv_output_selected_.set_node(node);
    light_enabled_.set_node(node);
    magnet_engaged_.set_node(node);
    voltage_.set_node(node);
  }
};

}  // namespace state_validate
}  // namespace dropbot_dx

#endif  // #ifndef ___DROPBOT_DX_STATE_VALIDATE___
    
