#include <turbodbc/parameter_sets/bound_parameter_set.h>

#include <turbodbc/make_description.h>

#include <stdexcept>
#include <sqlext.h>

namespace turbodbc {

namespace {
	std::size_t const max_initial_string_length = 16;

	std::shared_ptr<parameter> make_parameter(cpp_odbc::statement const & statement, std::size_t one_based_index, std::size_t buffered_sets)
	{
		auto description = make_description(statement.describe_parameter(one_based_index));
		if ((description->get_type_code() == type_code::string) and
		    (description->element_size() > (max_initial_string_length + 1)))
		{
			auto modified_description = statement.describe_parameter(one_based_index);
			modified_description.size = max_initial_string_length;
			description = make_description(modified_description);
		}
		return std::make_shared<parameter>(statement, one_based_index, buffered_sets, std::move(description));
	}
}


bound_parameter_set::bound_parameter_set(cpp_odbc::statement const & statement,
                                         std::size_t buffered_sets) :
		statement_(statement),
		buffered_sets_(buffered_sets),
		transferred_sets_(0),
		confirmed_last_batch_(0)
{
	std::size_t const n_parameters = statement_.number_of_parameters();
	for (std::size_t one_based_index = 1; one_based_index <= n_parameters; ++one_based_index) {
		parameters_.push_back(make_parameter(statement_, one_based_index, buffered_sets_));
	}
	statement_.set_attribute(SQL_ATTR_PARAMS_PROCESSED_PTR, &confirmed_last_batch_);
}

std::size_t bound_parameter_set::buffered_sets() const
{
	return buffered_sets_;
}

std::size_t bound_parameter_set::transferred_sets() const
{
	return transferred_sets_;
}


std::size_t bound_parameter_set::number_of_parameters() const
{
	return parameters_.size();
}


std::vector<std::shared_ptr<parameter>> const & bound_parameter_set::get_parameters()
{
	return parameters_;
}


void bound_parameter_set::execute_batch(std::size_t sets_in_batch)
{
	if ((sets_in_batch != 0) and not parameters_.empty()) {
		if (sets_in_batch <= buffered_sets_) {
			statement_.set_attribute(SQL_ATTR_PARAMSET_SIZE, sets_in_batch);
			statement_.execute_prepared();
			transferred_sets_ += confirmed_last_batch_;
		} else {
			throw std::logic_error("A batch cannot be larger than the number of buffered sets");
		}
	}
}


void bound_parameter_set::rebind(std::size_t parameter_index,
                                 std::unique_ptr<description const> parameter_description)
{
	parameters_[parameter_index] = std::make_shared<parameter>(statement_,
	                                                           parameter_index + 1,
	                                                           buffered_sets_,
	                                                           std::move(parameter_description));
}


}