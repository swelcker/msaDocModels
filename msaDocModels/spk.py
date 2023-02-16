import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from bson.objectid import ObjectId
from pydantic import UUID4, BaseModel, Field

from msaDocModels import sdu, wdc
from msaDocModels.sdu import (
    SDUAttachment,
    SDUContent,
    SDUData,
    SDUEmail,
    SDULanguage,
    SDUText,
)


class TenantIdInput(BaseModel):
    """Input model with tenant_id"""

    tenant_id: UUID4


class TextInput(BaseModel):
    """Input model with input_text"""

    input_text: Union[str, List, Dict]


class DocumentInput(TextInput):
    """Input document model"""

    document_id: Optional[UUID4]


class SentencesInput(BaseModel):
    """Input model with sentences"""

    document_id: Optional[UUID4]
    sentences: List[str]


class DocumentIds(BaseModel):
    """Ids of documents from mail model"""

    document_ids: List[str]


class DocumentLangInput(DocumentInput):
    """Input document model made over SDULanguage. Default language ENGLISH"""

    language: SDULanguage = SDULanguage(code="en", lang="ENGLISH")


class SPKLanguageInput(DocumentInput):
    """Input model to detect language."""

    hint_languages: str = ""
    hint_encoding: str = ""
    sentence_detection: bool = True
    get_vectors: bool = True
    is_plain_text: bool = True
    is_short_text: bool = False


class SPKLanguageDTO(sdu.SDULanguageDetails):
    """DTO, representing the result of service language."""


class TextWithParagraphsGet(BaseModel):
    """Schema representing the result of paragraph segmentation."""

    paragraphs: List[sdu.SDUParagraph]


class TextWithSentencesGet(BaseModel):
    """Schema representing the result of sentences segmentation."""

    sentences: List[sdu.SDUSentence]


class TextWithPagesGet(BaseModel):
    """Schema representing the result of pages segmentation."""

    pages: List[sdu.SDUPage]


class SPKSegmentationInput(BaseModel):
    """Input model to detect Segmentation"""

    document_id: Optional[UUID4]
    input_text: Union[str, List[str], Dict[int, str]]
    language: SDULanguage = SDULanguage(code="en", lang="ENGLISH")


class SPKSegmentationDTO(BaseModel):
    """DTO, representing the result of service segmentation. Only one attribute will be non-empty."""

    pages: List[sdu.SDUPage] = []
    paragraphs: List[sdu.SDUParagraph] = []
    sentences: List[sdu.SDUSentence] = []


class SPKTextCleanInput(DocumentInput):
    """Data input model for Text Clean."""


class SPKTextCleanDTO(BaseModel):
    """DTO, representing the result of service text clean."""

    text: str


class SPKTextCleanAIInput(BaseModel):
    """Data input model for Text AI Clean."""

    text: List[str]


class SPKTextCleanAIDTO(BaseModel):
    """DTO, representing the result of service ai text clean."""

    text: List[str]


class SPKSentimentInput(DocumentInput):
    """Data input model for Sentiment."""


class SPKSentimentDTO(BaseModel):
    """DTO, representing the result of service Sentiment."""

    neg: Optional[float]
    neu: Optional[float]
    pos: Optional[float]
    compound: Optional[float]
    error: Optional[str]


class SPKPhraseMiningInput(DocumentLangInput):
    """Data input model for Phrase mining."""


class SPKPhraseMiningDTO(BaseModel):
    """DTO, representing the result of Phrase mining."""

    phrases: List[Union[List, List[Union[str, int]]]]


class SPKWeightedKeywordsDTO(BaseModel):
    """DTO, representing the result of service Keywords."""

    keywords: List[Union[List, List[Union[str, int]]]]


class SPKSummaryInput(DocumentLangInput):
    """Data input model for Summary."""

    sum_ratio: float = 0.2
    sentences_count: int = 15
    lsa: bool = False
    corpus_size: int = 5000
    community_size: int = 5
    cluster_threshold: float = 0.65


class SPKStatisticsInput(DocumentLangInput):
    """Data input model for Statistics."""


class SPKStatisticsDTO(sdu.SDUStatistic):
    """DTO, representing the result of service Statistics."""


class SPKSummaryDTO(wdc.WDCItem):
    """DTO, representing the result of service Summary."""


class SPKNotaryInput(DocumentInput):
    """Data input model for Notary."""

    city: str = "Bremen"


class SPKNotary(BaseModel):
    """Detected Notary Pydantic Model."""

    sid: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    zip_code: Optional[str]
    city: Optional[str]
    office_city: Optional[str]
    official_location: Optional[str]
    address: Optional[str]
    additional_address: Optional[str]
    title: Optional[str]
    phone: Optional[str]
    complete_name_with_official_location: Optional[str]
    local_city: str = "Bremen"
    is_local_city: bool


class SPKNotaryWinnerDTO(SPKNotary):
    """DTO, representing the result of service Notary."""


class SPKCountry(BaseModel):
    """Detected Country Pydantic Model."""

    name: str
    official: str
    currencies: Dict[str, Dict[str, str]]
    capital: List[str]
    region: str
    subregion: str
    languages: Dict[str, str]
    latlng: List[int]
    flag: str
    calling_codes: List[str]


class SPKCompany(BaseModel):
    """Detected Company Pydantic Model."""

    rank: int
    company: str
    employees: str
    change_in_rank: str
    industry: str
    description: str
    revenue: str
    revenue_change: str
    profits: str
    profit_change: str
    assets: str
    market_value: str


class SPKCity(BaseModel):
    """Detected City Pydantic Model."""

    name: str
    country: str
    latlng: List[float]


class SPKTaxonomyCitiesDTO(BaseModel):
    """DTO, representing the result of service Taxonomy Cities."""

    cities: List[SPKCity]
    cities_winner: Optional[SPKCity]


class SPKTaxonomyCountriesDTO(BaseModel):
    """DTO, representing the result of service Taxonomy Countries."""

    countries: List[SPKCountry]
    countries_winner: Optional[SPKCountry]


class SPKTaxonomyCompaniesDTO(BaseModel):
    """DTO, representing the result of service Taxonomy Companies."""

    companies: List[SPKCompany]
    companies_winner: Optional[SPKCompany]


class SPKTaxonomyDTO(
    SPKTaxonomyCountriesDTO, SPKTaxonomyCompaniesDTO, SPKTaxonomyCitiesDTO
):
    """DTO, representing the result of service Taxonomy."""


class SPKTaxonomyInput(DocumentInput):
    """Data input model for Taxonomy."""


class AutoMLStatus(BaseModel):
    """
    Pydantic model to receive/send service status for pub/sub.

    Attributes:

        info: Service status.
        id: UUID model identifier.
        path: The path where model is located
    """

    info: str
    id: Optional[uuid.UUID]
    path: Optional[str]


class SPKProfileInput(BaseModel):
    """
    Pydantic model to generate a profile report based on data

    Attributes:
        title: Title of HTML representation.
        data: List of data.
        missing_diagrams: Settings related with the missing data section and the visualizations it can include.
        vars: Vars to provide another settings.
        correlations: Settings regarding correlation metrics and thresholds.
        sort: Default sorting.
        progress_bar: If True will display a progress bar.
        minimal: Minimal mode is a default configuration with minimal computation.
        explorative: Explorative mode.
        sensitive: Sensitive mode.
        dark_mode: Select a dar theme.
        orange_mode: Select a orange theme.

    """

    title: str
    html: Dict = {}
    missing_diagrams: Dict = {}
    correlations: Dict = {}
    vars: Dict = {}
    data: List[Dict[str, Any]]
    sort: str = "ascending"
    progress_bar: bool = False
    minimal: bool = False
    explorative: bool = False
    sensitive: bool = False
    dark_mode: bool = False
    orange_mode: bool = False


class SPKProfileDTO(BaseModel):
    """
    Pydantic model of Profile HTML representation
    """


class SPKBuildModelInput(BaseModel):
    """
    Model that contains input data for building a machine learning model.

    Attributes:

        model_name: The name of the model.
        data: The input data to be used for model training.
        target_columns: Column names representing the target variable(s) to be predicted.
        train_columns: Column names to be used for model training.
        text_features: Column names representing text features to be used for text processing.
        ignore_features: Column names representing features to be ignored during model training.
        categorical_features: Column names representing categorical features.
        date_features: Column names representing date features.
        numeric_features: Column names representing numeric features.
        ordinal_features: Dictionary of column names representing ordinal features and their categories.
        multiplier: Multiplier used for increasing the size of the training data using synthetic samples.
        session_id: Seed value used for reproducibility.
        remove_outliers: Flag indicating whether to remove outliers from the data.
        budget_time_minutes: Maximum time in minutes allowed for model training.
        included_engines: List of machine learning models to be used for model training.
        use_gpu: Flag indicating whether to use GPU for model training.
        fold: Number of folds for cross-validation.
        tuning_iterations: Number of iterations for hyperparameter tuning.
        create_metadata: Flag indicating whether to create model metadata
    """
    model_name: str = "kim_pipeline"
    data: List[Dict[str, Any]]
    target_columns: List[str] = []
    train_columns: List[str] = []
    text_features: List[str] = []
    ignore_features: List[str] = []
    categorical_features: List[str] = []
    date_features: List[str] = []
    numeric_features: List[str] = []
    ordinal_features: dict[str, list] = {}
    multiplier: int = 5
    session_id: int = 123
    remove_outliers: bool = False
    budget_time_minutes: float = 3.0
    included_engines: List[str] = ["svm", "nb", "ridge", "rf", "dt"]
    use_gpu = False
    fold: int = 7
    tuning_iterations: int = 7
    create_metadata = False


class SPKInferenceInput(BaseModel):
    """
     Pydantic model for get inference data.

    Attributes:

        path: The path where model is located.
        data: Profile html representation.
    """

    path: str
    data: List[Dict[str, Any]]


class SPKInferenceDTO(BaseModel):
    """
    Pydantic model, provided merged inference data.

    Attributes:

        inference: Raw data with inference data.
    """

    inference: List[Dict[str, Any]]


class ProcessStatus(BaseModel):
    """
    Workflow status

        Attributes:

        number: number of status
        timestamp: time when number was changes
    """

    number: int = 0
    timestamp: str = str(datetime.utcnow())


class SPKDBBaseDocumentInput(BaseModel):
    """
    Document fields for input.

    Attributes:

        uid: document uid
        name: document name.
        mimetype: mimetype.
        path: path to file.
        layout_file_path: path to layout file.
        debug_file_path: path to debug file.
        readorder_file_path: path to rearorder file.
        folder: folder name.
        group_uuid: group identifier.
        size_bytes: size in bytes.
        is_file: file or not.
        wfl_status: wfl status.
        import_status: import status.
        user: user name.
        date: date.
        runtime_s: runtime in sec.
        tags: list of tags.
        language: language.
        needs_update: need update or not.
        data: data.
        project_code: project code.
        npages: count of pages.
        content: content.
        metadata: metadata.
        description: discription.
        status: document status
        text: text.
        file: file.
        sdu: Dict of sdu objects.
    """

    uid: str
    name: str
    mimetype: str = "text/plain"
    path: str = ""
    layout_file_path: str = ""
    debug_file_path: str = ""
    readorder_file_path: str = ""
    folder: str = ""
    group_uuid: str = ""
    size_bytes: int = 0
    is_file: bool = False
    wfl_status: List = []
    import_status: str = "new"
    user: str = ""
    date: str = ""
    runtime_s: float = 0.0
    tags: Optional[Dict] = {}
    language: Optional[SDULanguage] = None
    needs_update: bool = False
    data: Optional[SDUData] = None
    project_code: str = ""
    npages: int = 0
    content: Optional[SDUContent] = None
    metadata: Dict = {}
    description: str = ""
    text: str = ""
    file: Dict = {}
    sdu: Dict = {}
    status: ProcessStatus = ProcessStatus()
    status_history: List[ProcessStatus] = [ProcessStatus()]


class PyObjectId(ObjectId):
    """
    Converts ObjectId to string.
    """

    @classmethod
    def __get_validators__(cls):
        """
        Generator to return validate method.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validates Object ID.

        Parameters:

             v: value to validate.

        Returns:

            Object ID with specified value.

        Raises:

            ValueError if Object ID does not pass validation.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoId(BaseModel):
    """
    MongoDB _id field.
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class SPKDBBaseDocumentDTO(SPKDBBaseDocumentInput, MongoId):
    """
    Document fields for output.
    """


class BaseInfo(BaseModel):
    """
    Base info for AI stuff.

    Attributes:

        version: version identifier.
        description: description.
        datetime: datetime.
        inherited: inherited or not.
        active: active or not.
        name: object name.
    """

    version: str
    description: str
    datetime: datetime
    inherited: bool
    active: bool
    name: str


class SPKUpdateAI(BaseModel):
    """
    Update ai fields.

    Attributes:

        version: version identifier.
        description: description.
        datetime: datetime.
        inherited: inherited or not.
        active: active or not.
        name: object name.
    """

    version: Optional[str]
    description: Optional[str]
    datetime: Optional[datetime]
    inherited: Optional[bool]
    active: Optional[bool]
    name: Optional[str]


class SPKLearnsetDataInput(BaseInfo):
    """
    AI learnset input.

    Attributes:

        learnsets: list of learnset objects.
    """

    learnsets: List[Dict]


class SPKTestsetDataInput(BaseInfo):
    """
    AI testset input.

    Attributes:

        testsets: list of testsets objects.
    """

    testsets: List[Dict]


class SPKTaxonomyDataInput(BaseInfo):
    """
    AI taxonomy input.

    Attributes:

        taxonomies: list of taxonomies objects.
    """

    taxonomies: List[Dict]


class SPKModelDataInput(BaseInfo):
    """
    AI model input.

    Attributes:

        model: model object.
    """

    model: Dict


class SPKTestsetDataDTO(SPKTestsetDataInput, MongoId):
    """
    AI testset output.
    """


class SPKLearnsetDataDTO(SPKLearnsetDataInput, MongoId):
    """
    AI learnset output.
    """


class SPKModelDataDTO(SPKModelDataInput, MongoId):
    """
    AI model output.
    """


class SPKTaxonomyDataDTO(SPKTaxonomyDataInput, MongoId):
    """
    AI taxonomy output.
    """


class SPKConversionInput(BaseModel):
    """
    Model that contains inference data along with filenames to use for XLSX conversion.

    Attributes:

        filenames: list of filenames that files should be saved as
        inference: inference data, first key means sheet name for XLSX file
    """

    filenames: List[str]
    inference: List[Dict[str, Dict[str, Any]]]


class SPKHTMLConverterResponse(BaseModel):
    """
    Response from converter

    Attributes:

        metadata: metadata from file
        txt_content: SDUText object
    """

    metadata: Dict
    txt_content: SDUText


class SPKEmailConverterResponse(BaseModel):
    content_attachments: List[SDUAttachment]
    txt_content: SDUText
    msg: SDUEmail
    content_unzipped_files: Optional[List[SPKHTMLConverterResponse]]


class FieldName(str, Enum):
    """Matching pydantic models with fields in the db.
    Attributes:
        TestsetDataInput: name of testset input model.
        LearnsetDataInput: name of learnset input model.
        ModelDataInput: name of model input model.
        TaxonomyDataInput: name of taxonomy input model.
    """

    TestsetDataInput = "testset"
    LearnsetDataInput = "learnset"
    ModelDataInput = "model"
    TaxonomyDataInput = "taxonomy"

def change_value(mydict: dict ):
    mydict["hello"] = 5

if __name__ == "__main__":
    a = {"hello": 3}
    print(a)
    change_value(a)
    print(a)
