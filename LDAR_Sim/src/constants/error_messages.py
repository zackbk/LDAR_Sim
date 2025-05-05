"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        error_messages.py
Purpose:     Holds error messages used throughout the program


This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.

You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""


class Input_Processing_Messages:
    GENERATOR_ERROR = (
        "{file} file in the generator folder is missing. "
        "Ensure the generator folder is correctly set up with the necessary files "
        "or delete the folder to regenerate the files."
    )

    INVALID_EMISSIONS_SOURCE_ERROR = "Invalid emissions source information for source {source_name}"

    MISSING_EMISSIONS_FILE_ERROR = (
        "Emissions file parameter is missing for the virtual world. "
        "Please provide a valid emissions file"
    )
    INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR = (
        "LDAR-Sim could not parse source file value: {value} from source:{source}."
        " Encountered exception: {exception}"
    )
    INVALID_EMISSIONS_VALUE: dict[str, str] = {
        "data": "Data Usage",
        "dist": "Distribution Type",
        "max_emis": "Maximum Emission Rate",
        "unit_amt": "Units (amount)",
        "unit_time": "Units (time)",
        "source": "Data source values",
    }

    MISSING_FILE_PATH_ERROR = "File {file_path} does not exist"
    MISSING_FILE_ERROR = "FileNotFoundError reading in file: {file}"
    GENERAL_FILE_READING_ERROR = "Error reading in file: {file}"
    EXPECTED_FILE_ERROR = "Expected file type: {file_type}"
    SPEC_FILE_READING_ERROR = "Error reading {file_type} file: {file}"

    MISSING_SITES_FILE_HEADER_ERROR = "The sites file is missing the column: {header}"

    NO_PERSISTENT_FIELD_FOR_SOURCES_WARNING = (
        "WARNING: The persistent field has not been provided for sources."
        "Assuming all sources are persistent."
    )

    ERR_MSG_UNKNOWN_SENS_TYPE = (
        "LDAR-Sim could not resolve the provided sensor type for method: {method}."
        " Please enter a valid sensor type and try again."
    )

    VALID_REPAIR_DELAY_TYPE_ERROR = (
        "Double check the contents of the repair delay file."
        " A numerical value was provided as a repair delay"
    )

    RELATIVE_FILE_PATH_ERROR = (
        "Note that relative file paths must be relative to the root directory (see User Manual)"
    )
    INVALID_PARAM_FILE_FORMAT = "Invalid parameter file format: {filename}"

    PARAMETER_INTERPRET_WARNING = (
        "Warning: parameter_level should be supplied to parameter files, LDAR-Sim "
        "interprets parameter files as simulation_settings level if unspecified"
    )
    PARAMETER_PARSING_ERROR = "Parameter_level of {level} is not possible to parse."
    MISSING_PARAMETER_LEVEL_ERROR = (
        "Parameter_level is missing from one or more of the input parameter files. "
        "If all file provided are intended to be parameter files,"
        " please add the correct parameter_level."
    )

    NO_PROGRAMS_WARNING = "No programs are supplied"

    MISSING_METHOD_ERROR = "Warning: The following method was specified, but not supplied: {method}"

    MISSING_ARGUMENT_ERROR = "Please provide at least one input argument"

    INVALID_NAME_ERROR = (
        "Invalid {level} name provided: {name}. " "Refer to the User Manual for further details."
    )
    MISSING_DEPLOYMENT_TYPE_ERROR = "Warning: Deployment type is missing for method: {method}"

    QUANTIFICATION_FILE_NOT_FOUND = (
        "Warning: Quantification file {quantification_file} not found in {input_dir}."
    )
    QUANTIFICATION_INVALID_COLUMN = (
        "Warning: Quantification column {quantification_column} not found in {quantification_file}."
    )
    INVALID_INTERACTION_PRIO_ERROR = (
        "Invalid interaction_priority of {priority} set for method: {method}"
    )


class Runtime_Warning_Messages:
    POTENTIAL_CREW_SHORTAGE_MESSAGE = (
        "Warning: LDAR-Sim has detected a potential for crew shortage for the method: {method}"
    )
    FOLLOW_UP_METHOD_CREW_ESTIMATION = (
        "Warning: LDAR-Sim has defaulted to a single crew for the following "
        "follow-up method: {method}. "
        "This may lead to crew shortages, please provide a crew count for this method"
        " if this is not intended."
    )
    PATH_TOO_LONG_WARNING = (
        "Warning: LDAR-Sim has detected file path lengths approaching or"
        " exceeding the windows path limit."
        " This may result in a File Not Found Exception During Runtime. "
        "Please refer to the Installation Guide Section 6 for information"
        " on how to avoid this issue."
    )


class Output_Processing_Messages:
    OPERAND_ADDITION_ERROR = "Unsupported operand type for addition"
    OPERAND_INPLACE_ADDITION_ERROR = "Unsupported operand type for in-place addition"

    DURATION_FACTOR_ERROR = "Duration factor must be between 0.0 and 1.0"


class Runtime_Error_Messages:
    NO_BASE_PROG_ERROR = "No baseline program input...Exiting sim"

    INVALID_REDUND_FILTER_ERROR = "Invalid Redundancy filter: {filter} for method: {method}"

    INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE = (
        "LDAR-Sim has detected an invalid method deployment type of:"
        "{deploy_type} for method: {method}"
    )


class Versioning_Messages:

    LEGACY_PARAMETER_WARNING = (
        "\nLDAR-Sim has detected an attempt to run a simulation model"
        " with legacy parameter files. \n\n"
        "If the goal is to reproduce previously modelled results"
        " using the legacy parameters, please download the version"
        " of LDAR-Sim used to produce those results.\n"
        "Versioned releases can be found at: https://github.com/LDAR-Sim/LDAR_Sim/releases.\n\n"
        "Otherwise, please visit: "
        "https://github.com/LDAR-Sim/LDAR_Sim/blob/master/ParameterMigrationGuide.md"
        " for guidance on how to update parameter files to the latest version.\n"
        "Please rerun the model once you have successfully"
        " migrated your parameters to the latest version. \n\n"
        "See https://github.com/LDAR-Sim/LDAR_Sim/blob/master/changelog.md"
        " to find a record of what has changed with LDAR-Sim\n"
    )
    NEWER_PARAMETER_WARNING = (
        "\nLDAR-Sim has detected an attempt to run a simulation model"
        " with newer parameter files. \n\n"
        "If the goal is to reproduce previously modelled results "
        "using newer parameters, please download the newer version "
        "of LDAR-Sim compatible with newer parameters.\n"
        "Versioned releases can be found at: https://github.com/LDAR-Sim/LDAR_Sim/releases.\n\n"
        "Otherwise, please visit: "
        "https://github.com/LDAR-Sim/LDAR_Sim/blob/master/ParameterMigrationGuide.md"
        " for guidance on how to update parameter files to the other versions.\n"
        "Please rerun the model once you have successfully"
        " migrated your parameters to the correct version. \n\n"
        "See https://github.com/LDAR-Sim/LDAR_Sim/blob/master/changelog.md"
        " to find a record of what has changed with LDAR-Sim\n"
    )
    MINOR_VERSION_MISMATCH_WARNING = (
        "\nLDAR-Sim has detected an attempt to run a simulation model"
        " with out of date parameter files. \n\n"
        "New Parameters may have been introduced since the creation "
        "of the parameter files currently in use.\n"
        "See https://github.com/LDAR-Sim/LDAR_Sim/blob/master/changelog.md"
        " to find a record of what has changed with LDAR-Sim\n"
    )

    MAJOR_VERSION_ONLY_WARNING = (
        "\nLDAR-Sim has detected an attempt to run a simulation model"
        " with a single number version. \n\n"
        "Standard parameter version numbers include a major and a minor "
        " version number, for example: 4.0. \n\n"
        "Please update the version to a valid version and rerun LDAR-Sim. \n\n"
    )

    VERSION_WARNING = (
        "Warning: interpreting parameters as "
        "version {current_version} because version key was missing"
    )


class Initialization_Messages:
    SOURCE_INFO_MISSING_KEY_MSG = "Missing required source information: {key}"
    POTENTIAL_SOURCE_CREATION_ERROR_MESSAGE = (
        "Error creating emissions sources, they were only partially defined. "
        "Please input a value for the parameter '{rep} {const}' and rerun the simulation."
    )
    INVALID_REPAIR_DELAY_COL_MSG = "Error, Invalid repair delay column provided: {key}"
    INVALID_REPAIR_DELAY_ERR_MSG = "Error, Invalid repair delay provided: {delay}"

    PLACEHOLDER_CREATION_WARNING_MESSAGE = (
        "Warning: Only {type} emissions sources were created for the site ID: {site}. "
        "Check the production rate(s) if this is not intended."
    )
    EMISSION_PRODUCTION_RATE_ERROR = (
        "No valid emissions production rates. Please check values and re-run the simulation."
    )
    BAD_EQUIPMENT_INPUT_ERROR = "Invalid equipment input: {}"

    SOURCE_CREATION_ERROR_MESSAGE = (
        "Invalid LDAR-Sim infrastructure inputs: Failure to read in sources infrastructure input"
    )
    PARAMETER_CREATION_ERROR_MESSAGE = (
        "Key {key} present in user defined parameters for {name}, but not in default parameters"
    )
    PARAMETER_TYPE_MISMATCH_ERROR_MESSAGE = (
        "Parameter type mismatch for {name}. \nDefault parameter: {default} is {def_type}"
        "\nTest parameter: {test} is {test_type}"
    )
    AWS_KEY_SEC_ERROR = (
        "AWS_KEY and AWS_SEC environment variables have not been set,"
        "refer to model documentation for configuration instructions."
    )
    ERA_AUTH_ERROR = "Authentication Failed or Server Unavailable. Exiting"
    SURVEY_FREQUENCY_ERROR = (
        "Warning: No survey frequency was provided for method '{method}' at site '{site}'"
    )


class SensitivityAnalysisMessages:
    INVALID_PARAMETER_LEVEL_ERROR = (
        "Parameter level {parameter_level} not recognized for sensitivity analysis."
    )
    MISSING_SENSITIVITY_INFO = "Missing required sensitivity analysis information: {key}"
    INVALID_SENSITIVITY_VARIATIONS_ERROR = "Invalid sensitivity analysis variations provided"


class ParameterInteractionMessages:
    INVALID_PARAMETER_LEVEL_ERROR = "Invalid parameter level: {level}"
